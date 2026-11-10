from species_tree_backend.task_run_subsystem.db_task_run_info import DbTaskRunInfo


# Запускает задачи парсера данных и прочие тяжеловесные задачи БД, написанные в файле parser/wiki_parser.py.
# Использует subprocesses для задач...
# ...и threads для асинхронного взаимодействия с ними (чтение логов, например, надолго замораживает поток)
class DbTaskManager:
    __instance = None

    def __init__(self):
        # Для паттерна "Singleton"
        DbTaskManager.__instance = self

        # Словарь с объектами информации для каждой задачи. Ключи - task_id.
        self.__task_run_infos = {}


    # ДЛЯ ДОСТУПА СНАРУЖИ ВСЕГДА используйте этот метод. Объект нашего класса должен быть ТОЛЬКО ОДИН на всё приложение!
    # Дело в том, что он запускает тяжеловесные задачи парсера и мониторит их, и нечего их запускать из двух объектов.
    @staticmethod
    def get_instance():
        if DbTaskManager.__instance is None:
            DbTaskManager.__instance = DbTaskManager()
        return DbTaskManager.__instance

    # =============================================
    # Публичные методы:
    # =============================================

    # Обрабатывает список tasks, добавляя к каждой состояние и кусок недавних логов
    def get_tasks_states(self, tasks: list) -> list:
        for task in tasks:
            task_run_info = self._get_or_create_task_run_info(task)
            task_run_info.fulfill_task_state()
        return tasks

    # Проходится по списку задач и запускает все помеченные для автозапуска и не завершённые
    def start_tasks_on_startup(self, tasks: list):
        for task in tasks:
            if bool(task["is_rerun_on_startup"]) or \
                    (bool(task["is_resume_on_startup"]) and not bool(task["is_success"])):
                self.start_one_task(task)

    def start_one_task(self, task: dict):
        task_run_info = self._get_or_create_task_run_info(task)
        task_run_info.start_task()

    def stop_one_task(self, task_id: int):
        task_run_info = self.__task_run_infos[task_id]
        task_run_info.stop_task()

    # =============================================
    # Далее внутренние методы класса:
    # =============================================

    def _get_or_create_task_run_info(self, task: dict) -> DbTaskRunInfo:
        task_id = int(task["id"])
        task_run_info = self.__task_run_infos.get(task_id, None)
        if not task_run_info:
            task_run_info = DbTaskRunInfo(task)
            self.__task_run_infos[task_id] = task_run_info
        return task_run_info

    def __del__(self):
        # (Не останавливаем вспомогательные потоки, т.к. они лишь потоки и потому всё равно лягут вместе с сервером)
        for task_run_info in self.__task_run_infos.values():
            if task_run_info.process:
                try:
                    task_run_info.process.kill()
                finally:
                    pass
        DbTaskManager.__instance = None
