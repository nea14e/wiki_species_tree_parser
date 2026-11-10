import os
import threading
import time
from threading import Thread
from typing import Optional
from multiprocessing import Process, Manager
from multiprocessing.queues import Queue

from django.db import connections

from config import Config
from parser.wiki_parser import main_from_web

PARSER_CWD = os.path.join("../..", "parser")  # Путь относительно db_task_manager
PARSER_PATH = os.path.join(PARSER_CWD, "wiki_parser.py")


class DbTaskRunInfo:
    def __init__(self, task_id: int):
        # Сам объект задачи
        self.task_id = task_id
        self.task: Optional[dict] = None
        # Процесс под задачу
        self.process: Optional[Process] = None
        # Очередь process_manager.Queue() для получения сообщений от процесса
        self.process_logs_queue: Optional[Queue] = None
        # Флаг, была ли задача завершена пользователем принудительно.
        # Нужен, чтобы не помечать их как завершённые успешно или с ошибкой, а оставить is_success = None
        self.is_killed_by_user = False
        # Флаг, что задача была запущена и уже завершилась (нормально или с ошибкой).
        # Нужен, чтобы помечать задачи как завершённые только по одному разу на каждый запуск
        self.is_finished = False
        # Последние куски логов stdout для каждой задачи.
        # list() из не более чем LOGS_KEEP_RECORDS_COUNT строк логов.
        self.recent_stdout_logs: list[str] = []  # ...логи из stdout
        self.recent_stderr_logs: list[str] = []  # ...логи из stderr
        # Вспомогательные потоки для взаимодействия с процессом:
        self.check_is_process_finished_thread: Optional[Thread] = None  # ...для проверки, когда он закончится
        self.read_process_logs_thread: Optional[Thread] = None  # ...для чтения логов из stdout

    # =============================================
    # Публичные методы класса:
    # =============================================

    def update_task_state(self, task: dict):
        self.task = task
        task["is_running_now"] = self._check_task_if_running()
        # При редактировании задачи выставлять галочку "Launch now" по умолчанию:
        task["is_launch_now"] = task["is_running_now"]
        task["recent_stdout"], task["recent_stderr"] = self._get_task_recent_logs()

    def start_task(self, task: dict):
        self.task = task
        # Останавливаем задачу, если надо:
        if self._check_task_if_running():
            self.stop_task()
        # Логи очищаем именно при старте задачи, чтобы после её окончания они ещё оставались:
        self.recent_stdout_logs = []
        self.recent_stderr_logs = []
        # Сбрасываем флаги
        self.is_killed_by_user = False
        self.is_finished = False
        if task["is_success"] is not None:
            self._mark_task_as_uncompleted()

        process_manager = Manager()

        args = self._get_args_from_task(task)
        args = Config.PARSER_ARGS_DELIMITER.join(['"' + arg + '"' for arg in args])

        queue = process_manager.Queue()
        self.process_logs_queue = queue

        process = Process(target=main_from_web, args=(args, queue,))
        self.process = process
        process.start()

        # Чтение логов из процесса по таймеру
        thread = threading.Thread(target=self._check_one_finished_thread, args=(self.task_id,))
        self.check_is_process_finished_thread = thread
        thread.start()

        # Чтение логов из процесса по таймеру
        thread = threading.Thread(target=self._read_one_stdout_thread, args=(self.task_id,))
        self.read_process_logs_thread = thread
        thread.start()

    def stop_task(self):
        if not self.process:
            return
        self.recent_stdout_logs.append("[Task has been stopped by user.]")
        self.is_killed_by_user = True
        self.is_finished = True

        self.process.kill()

        # Эти служебные потоки остановятся сами, когда им надо
        self.check_is_process_finished_thread = None
        self.read_process_logs_thread = None

    # =============================================
    # Приватные методы класса:
    # =============================================

    def _check_task_if_running(self):
        if self.is_finished:  # если задача была завершена (нормально или с ошибкой)
            return False
        if self.process is None:  # если задачу ещё не запускали (процесс под неё ещё не был создан)
            return False
        return self.process.is_alive()

    # Формирует из недавних логов что-то подходящее для просмотра по заданной задаче
    def _get_task_recent_logs(self):
        if self.process is None:
            return "This task has not been run since last Backend Server's launch.", ""
        if not self.recent_stdout_logs and not self.recent_stderr_logs:
            return "This task not formed any logs yet.", ""
        return ("\n".join(self.recent_stdout_logs).replace("\n", "<br/>"),
                "\n".join(self.recent_stderr_logs).replace("\n", "<br/>"))

    # Составляет аргументов строки для процесса парсера
    # (т.к. он изначально был рассчитан на самостоятельный запуск из консоли)
    def _get_args_from_task(self, task: dict):
        # args = [str(task["python_exe"]), PARSER_PATH]
        args = [PARSER_PATH]
        if Config.BACKEND_IS_USE_TEST_DB:
            args.append("test")
        else:
            args.append("no_test")
        stage = str(task["stage"])
        args.append(stage)
        if stage == "1":
            args.append(task["args"]["list_page_title"])
            if task["args"].get("proxy", None):
                args.append(task["args"]["proxy"])
        elif stage == "2":
            args.append(str(bool(task["args"]["skip_parsed_interval"])))
            args.append('"' + str(task["args"]["where"]) + '"')
            if task["args"].get("proxy", None):
                args.append(task["args"]["proxy"])
        elif stage == "3":
            args.append('"' + str(task["args"]["where"]) + '"')
        elif stage == "test_task":
            args.append(str(bool(task["args"]["will_success"])))
            args.append(str(float(task["args"]["timeout"])))
        return args

    # Определяет, что задача завершилась.
    # (Крутится в отдельном потоке для каждой запущенной задачи.
    # Останавливается сам, чуть позже её остановки.)
    def _check_one_finished_thread(self, task_id: int):
        while True:
            if not self._check_task_if_running():
                self.is_finished = True
                return
            time.sleep(Config.PROC_STATE_UPDATE_TIMER)

    # Читает логи процесса из stdout.
    # (Крутится в отдельном потоке для каждой запущенной задачи.
    # Останавливается сам, чуть позже её остановки.)
    def _read_one_stdout_thread(self, task_id: int):
        while True:
            while not self.process_logs_queue.empty():
                line = str(self.process_logs_queue.get())

                if line[:len(Config.LOGS_ERROR_PREFIX)] == Config.LOGS_ERROR_PREFIX:
                    self.recent_stderr_logs.append(line[len(Config.LOGS_ERROR_PREFIX):])
                else:
                    self.recent_stdout_logs.append(line)
                # не стираем предыдущие логи, если новых нет (когда процесс упал/завершился)
            else:
                if self.is_finished:  # если логи закончились и процесс завершился - прекратить их чтение
                    self._mark_task_as_completed()  # пометить задачу как завершённую (нормально или с ошибкой)
                    # Важно, что понять, завершилась ли задача с успехом, мы можем, только прочитав все её логи,
                    # что происходит в этом методе уже ПОСЛЕ завершения задачи. Поэтому _mark_task_as_completed() именно тут.
                    return

            log_overflow = len(self.recent_stdout_logs) - Config.LOGS_KEEP_LINES_COUNT
            if log_overflow > 0:
                self.recent_stdout_logs = self.recent_stdout_logs[log_overflow:]

            err_overflow = len(self.recent_stderr_logs) - Config.LOGS_KEEP_LINES_COUNT
            if err_overflow > 0:
                self.recent_stderr_logs = self.recent_stderr_logs[err_overflow:]

            time.sleep(Config.LOGS_UPDATE_TIMER)

    # Помечает в БД задачу как завершённую (нормально или с ошибкой).
    # Влияет на автозапуск задач при рестарте сервера.
    def _mark_task_as_completed(self):
        if self.is_killed_by_user:
            # Если завершена принудительно пользователем, то успех = None:
            is_success = None
        else:
            # Успех = лог ошибок пустой:
            is_success = len(self.recent_stderr_logs) == 0

        if self.task:
            # У автосгенерированных задач при выдаче на фронт берётся отсюда
            self.task["is_success"] = is_success

        conn = connections["default"]
        cur = conn.cursor()
        cur.execute("""
            UPDATE public.tasks
            SET is_success = %s
            WHERE id = %s;
        """, (is_success, self.task_id,))
        conn.commit()

    # Помечает в БД задачу как завершённую (нормально или с ошибкой).
    # Влияет на автозапуск задач при рестарте сервера.
    def _mark_task_as_uncompleted(self):
        conn = connections["default"]
        cur = conn.cursor()
        cur.execute("""
            UPDATE public.tasks
            SET is_success = NULL
            WHERE id = %s;
        """, (self.task_id,))
        conn.commit()