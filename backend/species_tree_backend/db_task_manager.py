import os
import subprocess
import threading

from django.db import connections

PARSER_CWD = os.path.join("..", "parser")
PARSER_PATH = os.path.join(PARSER_CWD, "wiki_parser.py")


# Запускает задачи парсера данных и прочие тяжеловесные задачи БД, написанные в файле parser/wiki_parser.py.
class DbTaskManager:
    __instance = None

    def __init__(self):
        DbTaskManager.__instance = self
        self.processes_running = {}  # словарь с самими объектами процессов. Ключ - task_id
        self.finished_ids = []  # это процессы, которые выдали какой-то код возврата. Обновляется с задержкой по таймеру.
        self.recent_logs = {}  # словарь с последним куском логов stdout/stderr для каждого процесса. Ключ - task_id
        self.update_recent_logs_thread = threading.Timer(5.0, self._update_recent_logs)  # Обновление логов/состояний процессов по таймеру
        self.update_recent_logs_thread.start()

    # Для доступа снаружи ВСЕГДА используйте этот метод. Объект нашего класса должен быть ТОЛЬКО ОДИН на всё приложение!
    # Дело в том, что он запускает тяжеловесные задачи парсера и мониторит их, и нечего их запускать из двух объектов.
    @staticmethod
    def get_instance():
        if DbTaskManager.__instance is None:
            DbTaskManager.__instance = DbTaskManager()
        return DbTaskManager.__instance

    # Обрабатывает список tasks, добавляя к каждой состояние и кусок недавних логов
    def get_tasks_states(self, tasks: list) -> list:
        for task in tasks:
            task["running_state"] = self.get_task_running_state(task["id"])
            task["recent_logs"] = self._get_task_recent_logs(task)
        return tasks

    # Проходится по списку задач и запускает все помеченные для автозапуска и не завершённые
    def start_tasks_on_startup(self, tasks: list):
        for task in tasks:
            if bool(task["is_run_on_startup"]) and not bool(task["is_completed"]):
                self.start_one_task(task)

    def start_one_task(self, task: dict):
        task_id = int(task["id"])
        if self.check_task_if_running(task_id):
            self.stop_one_task(task_id)
        args = self._get_args_from_task(task)
        proc = subprocess.Popen(args, cwd=PARSER_CWD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes_running[task_id] = proc

    def check_task_if_running(self, task_id: int):
        if task_id not in self.processes_running:
            return False
        proc = self.processes_running[task_id]
        return proc.poll() is None

    def get_task_running_state(self, task_id: int) -> str:
        if task_id not in self.processes_running:
            return "Not running"
        proc = self.processes_running[task_id]
        return_code = proc.poll()
        if return_code is None:
            return "Running..."
        return "Returned code: " + str(return_code)

    def stop_one_task(self, task_id: int):
        if task_id in self.processes_running:
            self.processes_running[task_id].kill()
            del self.processes_running[task_id]
            self.finished_ids.append(task_id)

    # Составление аргументов командной строки для процесса парсера
    # (т.к. он изанчально был расчитан на самостоятельный запуск из консоли)
    @staticmethod
    def _get_args_from_task(task: dict):
        args = [str(task["python_exe"]), PARSER_PATH]
        stage = str(task["stage"])
        args.append(stage)
        if stage == "0":
            if bool(task["args"]["is_test"]):
                args.append("test")
        elif stage == "1":
            args.append(task["args"]["from_title"])
            args.append(task["args"]["to_title"])
            if task["args"]["proxy"]:
                args.append(task["args"]["proxy"])
        elif stage == "2":
            args.append(bool(task["args"]["skip_parsed_interval"]))
            args.append('"' + str(task["args"]["where"]) + '"')
            if task["args"]["proxy"]:
                args.append(task["args"]["proxy"])
        elif stage == "3":
            args.append('"' + str(task["args"]["where"]) + '"')
        elif stage == "parse_language":
            args.append(task["args"]["lang_key"])
            args.append(bool(task["args"]["skip_parsed_interval"]))
            args.append('"' + str(task["args"]["where"]) + '"')
            if task["args"]["proxy"]:
                args.append(task["args"]["proxy"])
        return args

    # Обновление логов/состояний процессов по таймеру
    def _update_recent_logs(self):
        for task_id, proc in self.processes_running.items():

            if not self.check_task_if_running(task_id):
                if task_id not in self.finished_ids:
                    self._mark_task_as_completed(task_id)
                    self.finished_ids.append(task_id)  # удалить процесс из self.processes_running нельзя, т.к. цикл по нему, да и не надо

            log_content = proc.stdout.read().decode("utf-8")
            if log_content:  # не стираем предыдущие логи, если новых нет (когда процесс упал/завершился)
                self.recent_logs[task_id] = log_content

            err_content = proc.stderr.read().decode("utf-8")
            if err_content:  # не стираем предыдущие логи, если новых нет (когда процесс упал/завершился)
                self.recent_logs[task_id] = err_content
                self._set_task_error_message(task_id, err_content)

        self.update_recent_logs_thread = threading.Timer(5.0, self._update_recent_logs)
        self.update_recent_logs_thread.start()

    def _mark_task_as_completed(self, task_id: int):
        is_success = self.processes_running[task_id].poll() == 0

        conn = connections["default"]
        cur = conn.cursor()
        cur.execute("""
            UPDATE public.tasks
            SET is_completed = %s
            WHERE id = %s;
        """, (is_success, task_id,))

    @staticmethod
    def _set_task_error_message(task_id: int, error_message: str):
        conn = connections["default"]
        cur = conn.cursor()
        cur.execute("""
            UPDATE public.tasks
            SET last_crash_message = %s
            WHERE id = %s;
        """, (error_message, task_id,))

    def _get_task_recent_logs(self, task_id: int) -> str:
        if task_id not in self.processes_running:
            return "This task was not run."
        if task_id not in self.recent_logs:
            return "This task not formed any logs yet, wait for 30 seconds."
        return self.recent_logs[task_id]

    def __del__(self):
        self.update_recent_logs_thread.cancel()
        DbTaskManager.__instance = None
