import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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
        general_conn.close()

        # Подключаемся к нашей базе
        if not DbFunctions.conn:
            DbFunctions.conn = psycopg2.connect(
                "dbname='lifetree' user='" + DbFunctions.user + "' host='" + DbFunctions.host + "' password='" + DbFunctions.password + "'")
            DbFunctions.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Создаём в ней таблицы, если надо
        # Таблица с царствами
        cur = DbFunctions.conn.cursor()
        sql = "SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'kingdoms';"
        cur.execute(sql)
        if cur.rowcount == 0:
            cur = DbFunctions.conn.cursor()
            sql = "CREATE TABLE public.kingdoms (" \
                  "id serial NOT NULL" \
                  ", title text NOT NULL" \
                  ", href text NOT NULL" \
                  ", CONSTRAINT pk_kingdoms PRIMARY KEY(id)" \
                  ", CONSTRAINT uq_kingdoms_title UNIQUE (title)" \
                  ", CONSTRAINT uq_kingdoms_href UNIQUE (href)" \
                  ");"
            print(str(sql))
            cur.execute(sql)
            cur = DbFunctions.conn.cursor()
            sql = "INSERT INTO public.kingdoms (title, href) " \
                  "VALUES ('animals', 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83')," \
                  "       ('plants', 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D0%B0%D1%81%D1%82%D0%B5%D0%BD%D0%B8%D1%8F_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83')," \
                  "       ('mushrooms', 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D1%80%D0%B8%D0%B1%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83')," \
                  "       ('viruses', 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%92%D0%B8%D1%80%D1%83%D1%81%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83');"
            print(str(sql))
            cur.execute(sql)
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
                  ", href text NOT NULL" \
                  ", CONSTRAINT pk_list PRIMARY KEY(id)" \
                  ", CONSTRAINT fk_list_kingdom FOREIGN KEY (kingdom_id) REFERENCES public.kingdoms(id)" \
                  ", CONSTRAINT uq_list UNIQUE (kingdom_id, title)" \
                  ");"
            print(str(sql))
            cur.execute(sql)
        # Таблица с подробностями
        cur = DbFunctions.conn.cursor()
        sql = "SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'details';"
        cur.execute(sql)
        if cur.rowcount == 0:
            cur = DbFunctions.conn.cursor()
            sql = "CREATE TABLE public.details (" \
                  "id bigint NOT NULL" \
                  ", title text NOT NULL" \
                  ", type text NOT NULL" \
                  ", image_url text" \
                  ", parent_id bigint" \
                  ", CONSTRAINT pk_details PRIMARY KEY(id)" \
                  ", CONSTRAINT fk_details_id FOREIGN KEY(id) REFERENCES public.list(id)" \
                  ", CONSTRAINT fk_details_parent_id FOREIGN KEY(parent_id) REFERENCES public.list(id)" \
                  ");"
            print(str(sql))
            cur.execute(sql)

    @staticmethod
    def get_kingdom_url(kingdom_title):
        if not DbFunctions.conn:
            raise Exception("Сначала вызовите метод DbFunctions.init_db()!")

        # Узнаем url царства по его названию
        cur = DbFunctions.conn.cursor()
        sql = "SELECT href " \
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
    def add_list_item(kingdom_title, title, href):
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
        sql = "INSERT INTO public.list (kingdom_id, title, href) " \
              "VALUES ('" + str(kingdom_id) + "', '" + str(title) + "', '" + str(href) + "')" \
                                                                                         "ON CONFLICT ON CONSTRAINT uq_list DO UPDATE SET href = EXCLUDED.href;"
        print(str(sql))
        cur.execute(sql)


class DbListItemsIterator(DbFunctions):
    def __init__(self, query):
        self.conn1 = psycopg2.connect(
            "dbname='lifetree' user='" + DbFunctions.user + "' host='" + DbFunctions.host + "' password='" + DbFunctions.password + "'")
        self.cur1 = DbFunctions.conn.cursor()
        self.cur1.execute(query)

    def fetchone(self):
        return self.cur1.fetchone()

    def __del__(self):
        self.conn1.close()
