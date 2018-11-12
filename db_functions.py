import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DbFunctions:
    user = str("postgres")
    host = str("192.168.3.23")
    password = str("postgres")
    conn = None

    @staticmethod
    def init_db(kingdom_table_name):
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
        # Таблица с подробностями
        cur = DbFunctions.conn.cursor()
        sql = "SELECT 1 FROM pg_class tbl WHERE tbl.relname = 'details';"
        cur.execute(sql)
        if cur.rowcount == 0:
            cur = DbFunctions.conn.cursor()
            sql = "CREATE TABLE public.details (title text, href text);"
            print(str(sql))
            cur.execute(sql)
        # Таблица со списком
        cur = DbFunctions.conn.cursor()
        sql = "SELECT 1 FROM pg_class tbl WHERE tbl.relname = '" + str(kingdom_table_name) + "';"
        cur.execute(sql)
        if cur.rowcount == 0:
            cur = DbFunctions.conn.cursor()
            sql = "CREATE TABLE public." + str(kingdom_table_name) + " (title text, href text);"
            print(str(sql))
            cur.execute(sql)


DbFunctions.init_db('animals')