import json
import os

import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DbFunctions:
    user = str("postgres")
    # host = str("192.168.33.147")
    host = str("127.0.0.1")
    password = str("12345")
    db_name = None  # Смотрите на пару строк ниже
    default_conn_tag = "default_conn"

    @staticmethod
    def init_db(is_test: bool = False):
        if is_test:
            print("Инициализация тестовой базы lifetree_test...\n")
            DbFunctions.db_name = "lifetree_test"
        else:
            print("Инициализация основной базы lifetree...\n")
            DbFunctions.db_name = 'lifetree'

        # Подключаемся к базе данных по умолчанию, чтобы создать нашу базу, если надо
        general_conn = psycopg2.connect(
            "dbname='postgres' user='" + DbFunctions.user + "' host='" + DbFunctions.host + "' password='" + DbFunctions.password + "'")
        general_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = general_conn.cursor()
        sql = "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = '{}');".format(DbFunctions.db_name)
        cur.execute(sql)
        is_db_exists = bool(cur.fetchone()[0])
        if not is_db_exists:  # Если база данных ещё не создана
            sql = "CREATE DATABASE {};".format(DbFunctions.db_name)
            print(str(sql))
            cur.execute(sql)
        else:
            print("База {} уже существует, пропускаем этап создания.".format(DbFunctions.db_name))
        general_conn.close()


        print("\n\n===================================================")
        print("Создаём таблицы:")

        # Таблица со списком
        print("\nТаблица со списком:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'list');"
        is_list_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_list_table_exists:
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "list.sql"))
        else:
            print("Таблица public.list уже существует, пропускаем этап создания.")

        # Таблица с рангами
        print("\nТаблица с рангами:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'ranks');"
        is_ranks_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_ranks_table_exists:
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "ranks.sql"))
        else:
            print("Таблица public.ranks уже существует, пропускаем этап создания.")

        # Таблица с языками
        print("\nТаблица с языками:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'known_languages');"
        is_ranks_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_ranks_table_exists:
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "tables", "known_languages.sql"))
        else:
            print("Таблица public.known_languages уже существует, пропускаем этап создания.")

        # Заполняем данными
        print("\n\n===================================================")
        print("Заполняем данными:")
        if is_test:
            print("\nТаблица public.list (для теста)...")
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "list_TEST.sql"))
            print("\nТаблица public.ranks (для теста)...")
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "ranks_TEST.sql"))
        print("\nТаблица public.known_languages (для прода/теста)...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "known_languages_ANY.sql"))

        # Хранимки для выдачи данных
        # (триггерные функции надо писать в скрипте создания их таблицы)
        print("\n\n===================================================")
        print("Хранимки и прочие скрипты:")
        print("\nХранимка для выдачи дерева по умолчанию: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_tree_default.sql"))
        print("\nХранимка для выдачи дерева по id: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_tree_by_id.sql"))
        print("\nХранимка для подгрузки потомков дерева по id: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_childes_by_id.sql"))
        print("\nХранимка по поиску: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "search_by_words.sql"))
        print("\nХранимка по подсчёту листов в дереве: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "service_update_leaves_count.sql"))

        # Просто так
        print("\n\n===================================================")
        print("Просто так:")
        sql = "SELECT COUNT(1) FROM public.list;"
        list_records_count = DbListItemsIterator("init_db", sql).fetchone()[0]
        print("В таблице public.list сейчас {} записей.".format(list_records_count))

        print("\n\n===================================================")
        print("\n\n")

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
        db_list_iter = DbListItemsIterator(DbFunctions.default_conn_tag, sql)
        result_message = str(db_list_iter.fetchone()[0])
        db_list_iter.commit()  # Обязательно сохранить изменения, сделанные в этом соединении
        print("Обновление количества видов в каждом узле дерева успешно завершено. Сообщение из БД:")
        print(result_message)

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
            new_conn = psycopg2.connect("dbname='" + DbFunctions.db_name + "' user='" + DbFunctions.user + "' host='" + DbFunctions.host + "' password='" + DbFunctions.password + "'")
            cls.connections_pool[tag] = new_conn
            return new_conn


class DbListItemsIterator:
    def __init__(self, connection_tag, query):
        self.conn1 = DbConnectionsHandler.get_connection(connection_tag)
        self.cur1 = self.conn1.cursor()
        self.cur1.execute(query)

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
        cur1.execute(query)
        conn1.commit()

    @staticmethod
    def execute_file(connection_tag, path):
        print("execute_file(): ", path)
        with open(path, "r", encoding="utf-8") as f:
            query = f.read()
        conn1 = DbConnectionsHandler.get_connection(connection_tag)
        cur1 = conn1.cursor()
        cur1.execute(query)
        conn1.commit()


def quote_nullable(val):
    if val is None:
        return "null"
    else:
        return "'" + str(val).replace("'", "''") + "'"

def quote_string(val):
    return "'" + str(val).replace("'", "''") + "'"