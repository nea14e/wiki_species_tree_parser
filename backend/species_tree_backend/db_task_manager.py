import os
import threading
import time
from multiprocessing import Process, Manager

from django.db import connections

from parser.wiki_parser import main_from_web
from config import Config

PARSER_CWD = os.path.join("..", "parser")
PARSER_PATH = os.path.join(PARSER_CWD, "wiki_parser.py")




# Запускает задачи парсера данных и прочие тяжеловесные задачи БД, написанные в файле parser/wiki_parser.py.
# Использует subprocesses для задач...
# ...и threads для асинхронного взаимодействия с ними (чтение логов, например, надолго замораживает поток)
class DbTaskManager:
    __instance = None

    def __init__(self):
        # Для паттерна "Singleton"
        DbTaskManager.__instance = self

        # Словарь с самими объектами задач под каждую запущенную задачу. Ключи - task_id
        self.tasks = {}
        # Словарь с объектами процессов под каждую запущенную задачу. Ключи - task_id
        self.processes_running = {}
        # Словарь с очередями process_manager.Queue() для получения сообщений от задач. Ключи - task_id
        self.processes_logs = {}

        # Список id задач, процессы для которых были завершены пользователем принудительно
        # Нужен, чтобы не помечать их как завершённые успешно или с ошибкой, а оставить is_success = None
        self.killed_by_user_ids = []
        # Список id задач, процессы для которых были запущены и уже завершились (нормально или с ошибкой).
        # Нужен, чтобы помечать задачи как завершённые только по одному разу на каждый запуск
        self.finished_ids = []

        # Словари с последними кусками логов stdout для каждой задачи.
        # Ключи - task_id, значение - list() из не более чем LOGS_KEEP_RECORDS_COUNT строк логов.
        self.recent_stdout_logs = {}  # ...логи из stdout
        self.recent_stderr_logs = {}  # ...логи из stderr

        # Словари с запущенными вспомогательными потоками для взаимодействия с процессами от каждой задачи:
        self.check_one_finished_threads = {}  # ...для проверки, когда он закончится
        self.read_one_stdout_threads = {}  # ...для чтения логов из stdout

    # ДЛЯ ДОСТУПА СНАРУЖИ ВСЕГДА используйте этот метод. Объект нашего класса должен быть ТОЛЬКО ОДИН на всё приложение!
    # Дело в том, что он запускает тяжеловесные задачи парсера и мониторит их, и нечего их запускать из двух объектов.
    @staticmethod
    def get_instance():
        if DbTaskManager.__instance is None:
            DbTaskManager.__instance = DbTaskManager()
        return DbTaskManager.__instance

    # Обрабатывает список tasks, добавляя к каждой состояние и кусок недавних логов
    def get_tasks_states(self, tasks: list) -> list:
        for task in tasks:
            task["is_running_now"] = self._check_task_if_running(task["id"])
            task["is_launch_now"] = task["is_running_now"]  # При редактировании задачи выставлять галочку "Launch now" по умолчанию
            task["recent_stdout"], task["recent_stderr"] = self._get_task_recent_logs(task["id"])
        return tasks

    # Проходится по списку задач и запускает все помеченные для автозапуска и не завершённые
    def start_tasks_on_startup(self, tasks: list):
        for task in tasks:
            if bool(task["is_rerun_on_startup"]) or \
                    (bool(task["is_resume_on_startup"]) and not bool(task["is_success"])):
                self.start_one_task(task)

    def start_one_task(self, task: dict):
        task_id = int(task["id"])

        if self._check_task_if_running(task_id):  # останавливаем задачу, если надо
            self.stop_one_task(task_id)
        if task_id in self.recent_stdout_logs:  # логи очищаем именно при старте задачи, чтобы после её окончания они ещё оставались
            del self.recent_stdout_logs[task_id]
        self.recent_stdout_logs[task_id] = list()
        if task_id in self.recent_stderr_logs:
            del self.recent_stderr_logs[task_id]
        self.recent_stderr_logs[task_id] = list()
        if task_id in self.killed_by_user_ids:
            self.killed_by_user_ids.remove(task_id)
        if task_id in self.finished_ids:
            self.finished_ids.remove(task_id)

        if task["is_success"] is not None:
            self._mark_task_as_uncompleted(task_id)

        process_manager = Manager()

        args = self._get_args_from_task(task)
        args = Config.PARSER_ARGS_DELIMITER.join(['"' + arg + '"' for arg in args])

        queue = process_manager.Queue()
        self.processes_logs[task_id] = queue

        proc = Process(target=main_from_web, args=(args, queue,))
        self.processes_running[task_id] = proc
        proc.start()

        self.tasks[task_id] = task

        thread = threading.Thread(target=self._check_one_finished_thread, args=(task_id,))  # Обновление логов/состояний процессов по таймеру
        self.check_one_finished_threads[task_id] = thread
        thread.start()

        thread = threading.Thread(target=self._read_one_stdout_thread, args=(task_id,))  # Обновление логов/состояний процессов по таймеру
        self.read_one_stdout_threads[task_id] = thread
        thread.start()

    def _check_task_if_running(self, task_id: int):
        if task_id in self.finished_ids:  # если задача была завершена (нормально или с ошибкой)
            return False
        if task_id not in self.processes_running:  # если задачу ещё не запускали (процесс под неё ещё не был создан)
            return False
        return self.processes_running[task_id].is_alive()

    def stop_one_task(self, task_id: int):
        if task_id in self.processes_running:
            self.recent_stdout_logs[task_id].append("[Task has been stopped by user.]")
            self.killed_by_user_ids.append(task_id)
            self.finished_ids.append(task_id)

            self.processes_running[task_id].kill()

            if task_id in self.check_one_finished_threads:
                del self.check_one_finished_threads[task_id]  # служебный поток из этого словаря остановится сам, когда ему надо
            if task_id in self.read_one_stdout_threads:
                del self.read_one_stdout_threads[task_id]  # служебный поток из этого словаря остановится сам, когда ему надо

    # =============================================
    # Далее внутренние методы класса:
    # =============================================

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
            args.append(task["args"]["from_title"])
            args.append(task["args"]["to_title"])
            if task["args"].get("proxy", None):
                args.append(task["args"]["proxy"])
        elif stage == "2":
            args.append(str(bool(task["args"]["skip_parsed_interval"])))
            args.append('"' + str(task["args"]["where"]) + '"')
            if task["args"].get("proxy", None):
                args.append(task["args"]["proxy"])
        elif stage == "3":
            args.append('"' + str(task["args"]["where"]) + '"')
        elif stage == "parse_language":
            args.append(task["args"]["lang_key"])
            args.append(str(bool(task["args"]["skip_parsed_interval"])))
            args.append('"' + str(task["args"]["where"]) + '"')
            if task["args"].get("proxy", None):
                args.append(task["args"]["proxy"])
        elif stage == "test_task":
            args.append(str(bool(task["args"]["will_success"])))
            args.append(str(float(task["args"]["timeout"])))
        return args

    # Определяет, что задача завершилась.
    # (Крутится в отдельном потоке для каждой запущенной задачи.
    # Останавливается сам, чуть позже её остановки.)
    def _check_one_finished_thread(self, task_id: int):
        while True:
            if not self._check_task_if_running(task_id):
                if task_id not in self.finished_ids:
                    self.finished_ids.append(task_id)  # удалить процесс из self.processes_running нельзя, т.к. цикл по нему, да и не надо
                    return
            time.sleep(Config.PROC_STATE_UPDATE_TIMER)

    # Читает логи процесса из stdout.
    # (Крутится в отдельном потоке для каждой запущенной задачи.
    # Останавливается сам, чуть позже её остановки.)
    def _read_one_stdout_thread(self, task_id: int):
        while True:
            while not self.processes_logs[task_id].empty():
                line = str(self.processes_logs[task_id].get())

                if line[:len(Config.LOGS_ERROR_PREFIX)] != Config.LOGS_ERROR_PREFIX:
                    self.recent_stdout_logs[task_id].append(line)  # не стираем предыдущие логи, если новых нет (когда процесс упал/завершился)
                else:
                    self.recent_stderr_logs[task_id].append(line[len(Config.LOGS_ERROR_PREFIX):])
            else:
                if task_id in self.finished_ids:  # если логи закончились и процесс завершился - прекратить их чтение
                    self._mark_task_as_completed(task_id)  # пометить задачу как завершённую (нормально или с ошибкой)
                    # важно, что понять, завершилась ли задача с успехом, мы можем, только прочитав все её логи,
                    # что происходит в этом методе уже ПОСЛЕ завершения задачи. Поэтому _mark_task_as_completed() именно тут.
                    return

            log_overflow = len(self.recent_stdout_logs[task_id]) - Config.LOGS_KEEP_LINES_COUNT
            if log_overflow > 0:
                self.recent_stdout_logs[task_id] = self.recent_stdout_logs[task_id][log_overflow:]

            err_overflow = len(self.recent_stderr_logs[task_id]) - Config.LOGS_KEEP_LINES_COUNT
            if err_overflow > 0:
                self.recent_stderr_logs[task_id] = self.recent_stderr_logs[task_id][err_overflow:]

            time.sleep(Config.LOGS_UPDATE_TIMER)

    # Помечает в БД задачу как завершённую (нормально или с ошибкой), влияет на автозапуск задач при рестарте сервера.
    # Не вызывать при отмене задачи пользователем.
    def _mark_task_as_uncompleted(self, task_id: int):
        conn = connections["default"]
        cur = conn.cursor()
        cur.execute("""
            UPDATE public.tasks
            SET is_success = NULL
            WHERE id = %s;
        """, (task_id,))
        conn.commit()

    # Помечает в БД задачу как завершённую (нормально или с ошибкой), влияет на автозапуск задач при рестарте сервера.
    # Не вызывать при отмене задачи пользователем.
    def _mark_task_as_completed(self, task_id: int):
        if task_id in self.killed_by_user_ids:
            # если завершена принудительно пользователем, то успех = None
            is_success = None
        else:
            # успех = лог ошибок пустой
            is_success = len(self.recent_stderr_logs[task_id]) == 0

        self.tasks[task_id]["is_success"] = is_success  # у автосгенерированных задач при выдаче берётся отсюда

        conn = connections["default"]
        cur = conn.cursor()
        cur.execute("""
            UPDATE public.tasks
            SET is_success = %s
            WHERE id = %s;
        """, (is_success, task_id,))
        conn.commit()

    # Просто обновляем логи ошибок в БД.
    # Не уверен, что при выдаче чего-либо в stderr процесс обязательно завершится,
    # поэтому не буду писать сюда is_success = FALSE и завершать задачу
    @staticmethod
    def _set_task_error_message(task_id: int, error_message: str):
        conn = connections["default"]
        cur = conn.cursor()
        cur.execute("""
            UPDATE public.tasks
            SET last_crash_message = %s
            WHERE id = %s;
        """, (error_message, task_id,))
        conn.commit()

    # Формирует из недавних логов что-то подходящее для просмотра по заданной задаче
    def _get_task_recent_logs(self, task_id: int) -> (str, str):
        def get_logs_internal() -> (str, str):
            if task_id not in self.processes_running:
                return "This task was not run since last Backend Server's launch.", ""
            if task_id not in self.recent_stdout_logs:
                return "This task not formed any logs yet.", ""
            if len(self.recent_stderr_logs[task_id]) > 0:
                return "\n".join(self.recent_stdout_logs[task_id]), "\n".join(self.recent_stderr_logs[task_id])
            else:
                return "\n".join(self.recent_stdout_logs[task_id]), ""

        logs, err_logs = get_logs_internal()
        return logs.replace("\n", "<br/>"), err_logs.replace("\n", "<br/>")

    def __del__(self):
        # (Не останавливаем вспомогательные потоки, т.к. они лишь потоки и потому всё равно лягут вместе с сервером)
        for proc in self.processes_running.values():
            try:
                proc.kill()  # сабпроцессы тоже вроде бы без этого и так останавливаются, но на всякий случай
            finally:
                pass
        DbTaskManager.__instance = None
