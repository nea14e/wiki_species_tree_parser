import json
import os

import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv


class DbFunctions:
    user = str("postgres")
    host = str("192.168.33.147")
    # host = str("127.0.0.1")
    password = str("12345")
    conn = None

    @staticmethod
    def init_db(is_use_test_data: bool = False):
        # Подключаемся к базе данных по умолчанию, чтобы создать нашу базу, если надо
        general_conn = psycopg2.connect(
            "dbname='postgres' user='" + DbFunctions.user + "' host='" + DbFunctions.host + "' password='" + DbFunctions.password + "'")
        general_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = general_conn.cursor()
        sql = "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = 'lifetree');"
        cur.execute(sql)
        is_db_exists = bool(cur.fetchone()[0])
        if not is_db_exists:  # Если база данных ещё не создана
            sql = "CREATE DATABASE lifetree;"
            print(str(sql))
            cur.execute(sql)
        else:
            print("База lifetree уже существует, пропускаем этап создания.")
        general_conn.close()

        # Подключаемся к нашей базе
        if not DbFunctions.conn:
            DbFunctions.conn = psycopg2.connect(
                "dbname='lifetree' user='" + DbFunctions.user + "' host='" + DbFunctions.host + "' password='" + DbFunctions.password + "'")
            DbFunctions.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Создаём в ней таблицы, если надо
        # Наполняем их данными, если надо

        # Таблица со списком
        print("\n\n===================================================")
        print("Таблица со списком:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'list');"
        is_list_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_list_table_exists:
            sql = """
                CREATE TABLE public.list (
                    id bigserial NOT NULL
                    , title text NOT NULL
                    , page_url text NOT NULL
                    , type text
                    , image_url text
                    , wikipedias_by_languages jsonb DEFAULT '{}'::jsonb
                    , titles_by_languages jsonb DEFAULT '{}'::jsonb
                    , parent_page_url text
                    , parent_id bigint
                    , CONSTRAINT pk_list PRIMARY KEY (id)
                    , CONSTRAINT uq_page_url UNIQUE (page_url)
                    , CONSTRAINT fk_list_parent_id FOREIGN KEY (parent_id) REFERENCES public.list (id)
                );
            
                CREATE INDEX list_index
                  ON public.list (parent_id, "type");
                """
            print(str(sql))
            DbExecuteNonQuery.execute("init_db", sql)
        else:
            print("Таблица public.list уже существует, пропускаем этап создания.")

        # Заполняем данными
        if is_use_test_data:
            print("Таблица public.list: заполняем данными (для теста)...")
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "list_TEST.sql"))

        # Просто так
        sql = "SELECT COUNT(1) FROM public.list;"
        list_records_count = DbListItemsIterator("init_db", sql).fetchone()[0]
        print("В таблице public.list сейчас {} записей.".format(list_records_count))

        # Таблица с рангами
        print("\n\n===================================================")
        print("Таблица с рангами:")
        sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'ranks');"
        is_ranks_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
        if not is_ranks_table_exists:
            sql = """
            CREATE TABLE public.ranks
            (
                   type    text NOT NULL
                          CONSTRAINT ranks_pk PRIMARY KEY,
                   "order" int  NOT NULL,
                   titles_by_languages jsonb DEFAULT '{}'::jsonb
            );
            
            CREATE UNIQUE INDEX ranks_order_uindex
                   ON public.ranks ("order");
            """
            print(str(sql))
            DbExecuteNonQuery.execute("init_db", sql)
        else:
            print("Таблица public.ranks уже существует, пропускаем этап создания.")

        # Заполняем данными
        if is_use_test_data:
            print("Таблица public.ranks: заполняем данными (для теста)...")
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "ranks_TEST.sql"))
        else:
            print("Таблица public.ranks: заполняем данными (для прода)...")
            DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "fill_tables", "ranks.sql"))

        # Языки
        print("\n\n===================================================")
        print("Языки:")
        DbFunctions.add_language("en")
        DbFunctions.add_language("ru")

        # Хранимки
        print("\n\n===================================================")
        print("Хранимки и прочие скрипты:")
        print("\nГлавная хранимка - для выдачи дерева: перенакатываем...")
        DbExecuteNonQuery.execute_file("init_db", os.path.join("init_db", "functions", "get_tree.sql"))

    @staticmethod
    def add_language(lang_key: str):
        print("add_language(): добавляем язык, если его ещё нет: lang_key = '{}'...".format(lang_key))

        # В таблицу со списком
        sql = "CREATE INDEX IF NOT EXISTS ix_list_{} ON public.list ((titles_by_languages->>'{}'));" \
                .format(lang_key, lang_key)
        print(str(sql))
        DbExecuteNonQuery.execute("add_language", sql)

    @staticmethod
    def add_list_item(title, page_url):
        if not DbFunctions.conn:
            raise Exception("Сначала вызовите метод DbFunctions.init_db()!")

        # Добавляем новый элемент в список или обновляем уже существующий
        cur = DbFunctions.conn.cursor()
        sql = """
                INSERT INTO public.list (title, page_url)
                  VALUES ('{}', '{}')
                ON CONFLICT ON CONSTRAINT uq_page_url 
                  DO UPDATE 
                  SET title = EXCLUDED.title;
            """.format(str(title), str(page_url))
        # print(str(sql))    # debug only
        cur.execute(sql)

    @staticmethod
    def add_details_to_item(title, page_url, _type, image_url, wikipedias_by_languages, titles_by_languages, parent_page_url):
        if not DbFunctions.conn:
            raise Exception("Сначала вызовите метод DbFunctions.init_db()!")

        # Добавляем новый элемент в список или обновляем уже существующий
        cur = DbFunctions.conn.cursor()
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
        # print(str(sql))    # debug only
        cur.execute(sql)


class DbConnectionsHandler():
    connections_pool = {}

    @classmethod
    def get_connection(cls, tag):
        """
                Выдаёт соединение, соответствующее тегу.
                Запоминает его для переиспользования - для одного и того же тега всегда выдаётся одно и то же соединение.
                При необходимости создаёт новый элемент (для нового тега).
                :param tag: некий тег для различения соединений
                :return: соединение, соответствующее тегу.
                """
        if tag in cls.connections_pool.keys():
            return cls.connections_pool[str(tag)]
        else:
            new_conn = psycopg2.connect("dbname='lifetree' user='" + DbFunctions.user + "' host='" + DbFunctions.host + "' password='" + DbFunctions.password + "'")
            cls.connections_pool[str(tag)] = new_conn
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
        with open(path, "r") as f:
            query = f.read()
        conn1 = DbConnectionsHandler.get_connection(connection_tag)
        cur1 = conn1.cursor()
        cur1.execute(query)
        conn1.commit()


def quote_nullable(val):
    if val is None:
        return "null"
    else:
        return "'" + str(val) + "'"