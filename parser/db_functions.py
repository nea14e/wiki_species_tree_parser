import json
import os
import traceback

import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config
from .logger import Logger


class DbFunctions:
    db_name = None  # Смотрите на пару строк ниже
    default_conn_tag = "default_conn"

    @staticmethod
    def prepare_to_work(is_test: bool = False):
        if is_test:
            Logger.print("Подготовка работы с тестовой базой lifetree_test...\n")
            DbFunctions.db_name = "lifetree_test"
        else:
            Logger.print("Подготовка работы с основной базой lifetree...\n")
            DbFunctions.db_name = 'lifetree'

    @staticmethod
    def init_db(is_test: bool = False):
        DbFunctions.prepare_to_work(is_test)

        # Подключаемся к базе данных по умолчанию, чтобы создать нашу базу, если надо
        general_conn = psycopg2.connect("host='" + Config.DB_HOST + "' port=" + Config.DB_PORT +
            " dbname='postgres' user='" + Config.DB_USER + "' password='" + Config.DB_PASSWORD + "'")
        general_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = general_conn.cursor()
        sql = "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = '{}');".format(DbFunctions.db_name)
        cur.execute(sql)
        is_db_exists = bool(cur.fetchone()[0])
        if not is_db_exists:  # Если база данных ещё не создана
            sql = "CREATE DATABASE {};".format(DbFunctions.db_name)
            Logger.print(str(sql))
            cur.execute(sql)
        else:
            Logger.print("База {} уже существует, пропускаем этап создания.".format(DbFunctions.db_name))
        general_conn.close()


        Logger.print("\n\n===================================================")
        Logger.print("Создаём таблицы:")

        # Таблица со списком
        Logger.print("\nТаблица со списком:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'list');"
        is_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_table_exists:
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "list.sql"))
        else:
            Logger.print("Таблица public.list уже существует, пропускаем этап создания.")
        Logger.print("Миграция public.list_MIGRATE...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "list_MIGRATE.sql"))

        # Таблица с рангами
        Logger.print("\nТаблица с рангами:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'ranks');"
        is_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_table_exists:
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "ranks.sql"))
        else:
            Logger.print("Таблица public.ranks уже существует, пропускаем этап создания.")

        # Таблица с языками
        Logger.print("\nТаблица с языками:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'known_languages');"
        is_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_table_exists:
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "known_languages.sql"))
        else:
            Logger.print("Таблица public.known_languages уже существует, пропускаем этап создания.")
        Logger.print("Миграция public.known_languages_MIGRATE...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "known_languages_MIGRATE.sql"))
        Logger.print("Миграция public.known_languages_MIGRATE_2...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "known_languages_MIGRATE_2.sql"))

        # Таблица с советами дня
        Logger.print("\nТаблица с советами дня:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'tips_of_the_day');"
        is_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_table_exists:
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "tips_of_the_day.sql"))
        else:
            Logger.print("Таблица public.tips_of_the_day уже существует, пропускаем этап создания.")
        Logger.print("\nТаблица с советами дня: добавление колонки page_url:")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "tips_of_the_day_ADD_page_url.sql"))

        # Таблица с запущенными задачами
        Logger.print("\nТаблица с запущенными задачами:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'tasks');"
        is_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_table_exists:
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "tasks.sql"))
        else:
            Logger.print("Таблица public.tasks уже существует, пропускаем этап создания.")

        # Таблица с админ-пользователями
        Logger.print("\nТаблица с админ-пользователями:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'admin_users');"
        is_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_table_exists:
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "admin_users.sql"))
        else:
            Logger.print("Таблица public.admin_users уже существует, пропускаем этап создания.")

        # Заполняем данными
        Logger.print("\n\n===================================================")
        Logger.print("Заполняем данными:")
        if is_test:
            Logger.print("\nТаблица public.list (для теста)...")
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "list_TEST.sql"))
            Logger.print("\nТаблица public.ranks (для теста)...")
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "ranks_TEST.sql"))
        Logger.print("\nТаблица public.known_languages (для прода/теста)...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "known_languages_ANY.sql"))
        Logger.print("\nТаблица public.known_languages (для прода/теста) - выбор основного языка для администрирования...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "known_languages_ANY_set_main.sql"))
        if is_test:
            Logger.print("\nТаблица public.tips_of_the_day (для теста)...")
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "tips_of_the_day_TEST.sql"))
        else:
            Logger.print("\nТаблица public.tips_of_the_day (для прода)...")
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "tips_of_the_day_PROD.sql"))

        # Хранимки для выдачи данных
        # (триггерные функции надо писать в скрипте создания их таблицы)
        Logger.print("\n\n===================================================")
        Logger.print("Хранимки и прочие скрипты:")
        Logger.print("\nХранимка по выдаче перевода...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_translations.sql"))
        Logger.print("\nХранимка для выдачи дерева по умолчанию: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_tree_default.sql"))
        Logger.print("\nХранимка для выдачи дерева по id: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_tree_by_id.sql"))
        Logger.print("\nХранимка для подгрузки потомков дерева по id: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_childes_by_id.sql"))
        Logger.print("\nХранимка по поиску: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "search_by_words.sql"))
        Logger.print("\nХранимка по выдаче совета дня...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_tip_of_the_day.sql"))
        Logger.print("\nХранимка по выдаче совета дня по id...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_tip_of_the_day_by_id.sql"))
        Logger.print("\nХранимка по подсчёту листов в дереве: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "service_update_leaves_count.sql"))
        Logger.print("\nХранимка по проверке прав пользователей-админов: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "check_rights.sql"))
        Logger.print("\nХранимка по выдаче советов для перевода: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_all_tips_translations.sql"))

        # Просто так
        Logger.print("\n\n===================================================")
        Logger.print("Просто так:")
        sql = "SELECT COUNT(1) FROM public.list;"
        list_records_count = DbListItemsIterator("init_db", sql).fetchone()[0]
        Logger.print("В таблице public.list сейчас {} записей.".format(list_records_count))

        Logger.print("\n\n===================================================")
        Logger.print("\n\n")

    @staticmethod
    def add_list_item(title, page_url):
        # Добавляем новый элемент в список или обновляем уже существующий
        sql = """
                INSERT INTO public.list (title, page_url)
                  VALUES ('{}', '{}')
                ON CONFLICT ON CONSTRAINT uq_page_url 
                  DO UPDATE 
                  SET title = EXCLUDED.title;
            """.format(str(title), str(page_url))
        DbExecuteNonQuery.execute(DbFunctions.default_conn_tag, sql)

    @staticmethod
    def add_details_to_item(title, page_url, _type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url):
        # Добавляем новый элемент в список или обновляем уже существующий
        sql = """
                UPDATE public.list
                SET
                  title = '{}'
                  , type = '{}'
                  , image_url = '{}'
                  , wikipedias_by_languages = '{}'
                  , titles_by_languages = '{}'
                  , parent_page_url = '{}'
                WHERE page_url = '{}';
            """.format(
                str(title)
                , str(_type)
                , str(image_url)
                , json.dumps(wikipedias_by_languages)
                , json.dumps(titles_by_languages)
                , str(parent_page_url)
                , str(page_url)
            )
        DbExecuteNonQuery.execute(DbFunctions.default_conn_tag, sql)

    @staticmethod
    def update_leaves_count():
        # Обновление количества видов в каждом узле дерева
        sql = """
                SELECT public.service_update_leaves_count();
            """
        print(sql)
        db_list_iter = DbListItemsIterator(DbFunctions.default_conn_tag, sql)
        result_message = str(db_list_iter.fetchone()[0])
        db_list_iter.commit()  # Обязательно сохранить изменения, сделанные в этом соединении
        Logger.print("Обновление количества видов в каждом узле дерева успешно завершено. Сообщение из БД:")
        Logger.print(result_message)

class DbConnectionsHandler:
    connections_pool = {}

    @classmethod
    def get_connection(cls, tag: str = "default_conn"):
        """
                Выдаёт соединение, соответствующее тегу.
                Запоминает его для переиспользования - для одного и того же тега всегда выдаётся одно и то же соединение.
                При необходимости создаёт новый элемент (для нового тега).
                :param tag: str: некий тег для различения соединений
                :return: соединение, соответствующее тегу.
                """
        if tag in cls.connections_pool.keys():
            return cls.connections_pool[tag]
        else:
            new_conn = psycopg2.connect("host='" + Config.DB_HOST + "' port=" + Config.DB_PORT + " dbname='" + DbFunctions.db_name + "' user='" + Config.DB_USER + "' password='" + Config.DB_PASSWORD + "'")
            cls.connections_pool[tag] = new_conn
            return new_conn


class DbListItemsIterator:
    def __init__(self, connection_tag, query):
        self.conn1 = DbConnectionsHandler.get_connection(connection_tag)
        self.cur1 = self.conn1.cursor()
        try:
            self.cur1.execute(query)
            self.conn1.commit()
        except BaseException:
            error_message = traceback.format_exc()
            for line in error_message.split("\n"):
                Logger.print(Config.LOGS_ERROR_PREFIX + line)
            self.conn1.rollback()

    def rowcount(self):
        return self.cur1.rowcount

    def fetchone(self):
        return self.cur1.fetchone()

    def commit(self):
        self.conn1.commit()


class DbExecuteNonQuery:
    @staticmethod
    def execute(connection_tag, query):
        conn1 = DbConnectionsHandler.get_connection(connection_tag)
        cur1 = conn1.cursor()
        try:
            cur1.execute(query)
            conn1.commit()
        except BaseException:
            error_message = traceback.format_exc()
            for line in error_message.split("\n"):
                Logger.print(Config.LOGS_ERROR_PREFIX + line)
            conn1.rollback()

    @staticmethod
    def execute_file(connection_tag, path):
        Logger.print("execute_file(): ", path)
        # path is relative to this script file's directory, not to the root script
        this_script_file = os.path.realpath(__file__)
        this_script_dir = os.path.dirname(this_script_file)
        path = os.path.join(this_script_dir, path)
        with open(path, "r", encoding="utf-8") as f:
            query = f.read()
        conn1 = DbConnectionsHandler.get_connection(connection_tag)
        cur1 = conn1.cursor()
        try:
            cur1.execute(query)
            conn1.commit()
        except BaseException:
            error_message = traceback.format_exc()
            for line in error_message.split("\n"):
                Logger.print(Config.LOGS_ERROR_PREFIX + line)
            conn1.rollback()


def quote_nullable(val):
    if val is None:
        return "null"
    else:
        return "'" + str(val).replace("'", "''") + "'"

def quote_string(val):
    return "'" + str(val).replace("'", "''") + "'"
