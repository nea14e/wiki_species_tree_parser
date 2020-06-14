import json
import os
import sqlite3


class DbFunctions:
    DB_FILE_PATH = "db.sqlite"
    conn = None

    @staticmethod
    def init_db():
        DbFunctions.conn = sqlite3.connect(DbFunctions.DB_FILE_PATH)
        # Создаём в ней таблицы
        # Наполняем их данными

        # Таблица со списком
        sql = """
            CREATE TABLE list (
                id bigserial NOT NULL
                , title text NOT NULL
                , page_url text NOT NULL
                , type text
                , image_url text
                , wikipedias_by_languages json DEFAULT '{}'
                , parent_page_url text
                , parent_id bigint
                , titles_by_languages json DEFAULT '{}'
                , CONSTRAINT pk_list PRIMARY KEY (id) ON CONFLICT REPLACE
                , CONSTRAINT uq_page_url UNIQUE (page_url) ON CONFLICT REPLACE
                , CONSTRAINT fk_list_parent_id FOREIGN KEY (parent_id) REFERENCES list (id)
            );
            """
        print(str(sql))
        DbExecuteNonQuery.execute("init_db", sql)

        # Просто так
        sql = "SELECT COUNT(1) FROM list;"
        list_count = DbListItemsIterator("init_db", sql).fetchone()[0]
        print("В таблице list сейчас {} записей.".format(list_count))

        # Хранимки
        DbExecuteNonQuery.execute_file("init_db", os.path.join("db_init", "functions", "get_tree.sql"))

    @staticmethod
    def add_list_item(title, page_url):
        if not DbFunctions.conn:
            raise Exception("Сначала вызовите метод DbFunctions.init_db()!")

        # Добавляем новый элемент в список или обновляем уже существующий
        cur = DbFunctions.conn.cursor()
        sql = """
                INSERT INTO list (title, page_url)
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
            new_conn = sqlite3.connect(DbFunctions.DB_FILE_PATH)
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
        return "'" + str(val).replace("'", "''") + "'"

def nonquoted_nullable(val):
    if val is None:
        return "null"
    else:
        return str(val)
