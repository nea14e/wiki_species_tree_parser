import json

import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv


class DbFunctions:
    user = str("postgres")
    # host = str("192.168.3.23")
    host = str("127.0.0.1")
    password = str("12345")
    conn = None

    @staticmethod
    def init_db():
        # Подключаемся к базе данных по умолчанию, чтобы создать нашу базу, если надо
        general_conn = psycopg2.connect(
            "dbname='postgres' user='" + DbFunctions.user + "' host='" + DbFunctions.host + "' password='" + DbFunctions.password + "'")
        general_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = general_conn.cursor()
        sql = "SELECT 1 FROM pg_database WHERE datname = 'lifetree';"
        cur.execute(sql)
        if cur.rowcount == 0:  # Если база данных ещё не создана
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
        cur = DbFunctions.conn.cursor()
        sql = "SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'list';"
        cur.execute(sql)
        if cur.rowcount == 0:
            cur = DbFunctions.conn.cursor()
            sql = """
                CREATE TABLE public.list (
                    id bigserial NOT NULL
                    , title text NOT NULL
                    , page_url text NOT NULL
                    , type text
                    , image_url text
                    , wikipedias_by_languages json DEFAULT '{}'
                    , parent_page_url text
                    , parent_id bigint
                    , CONSTRAINT pk_list PRIMARY KEY (id)
                    , CONSTRAINT uq_page_url UNIQUE (page_url)
                    , CONSTRAINT fk_list_parent_id FOREIGN KEY (parent_id) REFERENCES public.list (id)
                );
                """
            print(str(sql))
            cur.execute(sql)
        else:
            print("Таблица public.list уже существует, пропускаем этап создания.")

        # Просто так
        cur = DbFunctions.conn.cursor()
        sql = "SELECT COUNT(1) FROM public.list;"
        cur.execute(sql)
        list_count = cur.fetchone()[0]
        print("В таблице public.list сейчас {} записей.".format(list_count))

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
    def add_details_to_item(title, page_url, _type, image_url, wikipedias_by_languages, parent_page_url):
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
                  , parent_page_url = '{}'
                WHERE page_url = '{}';
            """.format(
                str(title)
                , str(_type)
                , str(image_url)
                , json.dumps(wikipedias_by_languages)
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


def quote_nullable(val):
    if val is None:
        return "null"
    else:
        return "'" + str(val) + "'"