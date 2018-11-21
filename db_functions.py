import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv


class DbFunctions:
    user = str("postgres")
    host = str("192.168.3.23")
    password = str("postgres")
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

        # Таблица с царствами
        cur = DbFunctions.conn.cursor()
        sql = "SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'kingdoms';"
        cur.execute(sql)
        if cur.rowcount == 0:
            cur = DbFunctions.conn.cursor()
            sql = "CREATE TABLE public.kingdoms (" \
                  "id serial NOT NULL" \
                  ", title text NOT NULL" \
                  ", list_url text NOT NULL" \
                  ", CONSTRAINT pk_kingdoms PRIMARY KEY(id)" \
                  ", CONSTRAINT uq_kingdoms_title UNIQUE (title)" \
                  ", CONSTRAINT uq_kingdoms_href UNIQUE (list_url)" \
                  ");"
            print(str(sql))
            cur.execute(sql)
        else:
            print("Таблица public.kingdoms уже существует, пропускаем этап создания.")
        # Данные о списках для парсинга (например, царствах).
        # Они не содержатся на Википедии ни в каком явном списке, поэтому вбиваются сюда фиксированно
        cur = DbFunctions.conn.cursor()
        sql = "SELECT COUNT(1) FROM public.kingdoms;"
        cur.execute(sql)
        if cur.fetchone()[0] == 0:
            cur = DbFunctions.conn.cursor()
            with open('db_init/kingdoms.csv', 'r') as csv_file:
                csv_content = csv.reader(csv_file)
                for ind, row in enumerate(csv_content):
                    if ind == 0:
                        continue
                    sql = "INSERT INTO public.kingdoms (id, title, list_url) " \
                          "VALUES (%s, '%s', '%s');" % (row[0], row[1], row[2])
                    print(str(sql))
                    cur.execute(sql)
            cur = DbFunctions.conn.cursor()
            sql = "select setval('kingdoms_id_seq', (select max(id) from public.kingdoms), true)"
            print(str(sql))
            cur.execute(sql)
        else:
            print("Таблица public.kingdoms уже наполнена, пропускаем этап заполнения.")

        # Таблица со списком
        cur = DbFunctions.conn.cursor()
        sql = "SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'list';"
        cur.execute(sql)
        if cur.rowcount == 0:
            cur = DbFunctions.conn.cursor()
            sql = "CREATE TABLE public.list (" \
                  "id bigserial NOT NULL" \
                  ", kingdom_id int NOT NULL" \
                  ", title text NOT NULL" \
                  ", page_url text NOT NULL" \
                  ", type text" \
                  ", image_url text" \
                  ", parent_title text" \
                  ", parent_id bigint" \
                  ", CONSTRAINT pk_list PRIMARY KEY(id)" \
                  ", CONSTRAINT fk_list_kingdom FOREIGN KEY (kingdom_id) REFERENCES public.kingdoms(id)" \
                  ", CONSTRAINT uq_list UNIQUE (kingdom_id, title)" \
                  ", CONSTRAINT fk_list_parent_id FOREIGN KEY(parent_id) REFERENCES public.list(id)" \
                  ");"
            print(str(sql))
            cur.execute(sql)
        else:
            print("Таблица public.list уже существует, пропускаем этап создания.")
        # Данные для корня дерева.
        # Они не содержатся на Википедии ни в каком явном списке, поэтому вбиваются сюда фиксированно
        cur = DbFunctions.conn.cursor()
        sql = "SELECT COUNT(1) FROM public.list;"
        cur.execute(sql)
        if cur.fetchone()[0] == 0:
            cur = DbFunctions.conn.cursor()
            with open('db_init/list.csv', 'r') as csv_file:
                csv_content = csv.reader(csv_file)
                for ind, row in enumerate(csv_content):
                    if ind == 0:
                        continue
                    sql = "INSERT INTO public.list (id, kingdom_id, title, page_url, type, image_url, parent_id) " \
                          "VALUES (%s, %s, '%s', '%s', '%s', '%s', %s);" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    print(str(sql))
                    cur.execute(sql)
            cur = DbFunctions.conn.cursor()
            sql = "select setval('list_id_seq', (select max(id) from public.list), true)"
            print(str(sql))
            cur.execute(sql)
        else:
            print("Таблица public.list уже наполнена, пропускаем этап заполнения.")

    @staticmethod
    def get_kingdom_url(kingdom_title):
        if not DbFunctions.conn:
            raise Exception("Сначала вызовите метод DbFunctions.init_db()!")

        # Узнаем url царства по его названию
        cur = DbFunctions.conn.cursor()
        sql = "SELECT list_url " \
              "FROM public.kingdoms " \
              "WHERE title = '" + str(kingdom_title) + "';"
        print(str(sql))
        cur.execute(sql)
        try:
            kingdom_url = cur.fetchone()[0]
            print('kingdom_url = ' + str(kingdom_url))
        except:
            raise Exception("Царство не найдено: " + str(kingdom_title))
        return kingdom_url

    @staticmethod
    def get_kingdom_id(kingdom_title):
        if not DbFunctions.conn:
            raise Exception("Сначала вызовите метод DbFunctions.init_db()!")

        # Узнаем id царства по его названию
        cur = DbFunctions.conn.cursor()
        sql = "SELECT id " \
              "FROM public.kingdoms " \
              "WHERE title = '" + str(kingdom_title) + "';"
        print(str(sql))
        cur.execute(sql)
        try:
            kingdom_id = cur.fetchone()[0]
            print('kingdom_id = ' + str(kingdom_id))
        except:
            raise Exception("Царство не найдено: " + str(kingdom_title))
        return kingdom_id

    @staticmethod
    def add_list_item(kingdom_title, title, page_url):
        if not DbFunctions.conn:
            raise Exception("Сначала вызовите метод DbFunctions.init_db()!")

        # Узнаем id царства по его названию
        cur = DbFunctions.conn.cursor()
        sql = "SELECT id " \
              "FROM public.kingdoms " \
              "WHERE title = '" + str(kingdom_title) + "';"
        print(str(sql))
        cur.execute(sql)
        try:
            kingdom_id = cur.fetchone()[0]
        except:
            raise Exception("Царство не найдено: " + str(kingdom_title))

        # Добавляем новый элемент в список или обновляем уже существующий
        cur = DbFunctions.conn.cursor()
        sql = "INSERT INTO public.list (kingdom_id, title, page_url) " \
              "VALUES ('" + str(kingdom_id) + "', '" + str(title) + "', '" + str(page_url) + "')" \
                                                                                         "ON CONFLICT ON CONSTRAINT uq_list DO UPDATE SET page_url = EXCLUDED.page_url;"
        print(str(sql))
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


def quote_nullable(val):
    if val is None:
        return "null"
    else:
        return "'" + str(val) + "'"