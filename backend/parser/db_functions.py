import json
import os
import traceback

import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config
from .db_execute_non_query import DbExecuteNonQuery
from .db_list_items_iterator import DbListItemsIterator
from .logger import Logger


class DbFunctions:
    default_conn_tag = "default_conn"

    @staticmethod
    def init_db():
        is_test = Config.BACKEND_IS_USE_TEST_DB
        if is_test:
            Logger.print("Подготовка работы с тестовой базой {}...\n".format(Config.TEST_DB_NAME))
            db_name = Config.TEST_DB_NAME
        else:
            Logger.print("Подготовка работы с основной базой {}...\n".format(Config.PROD_DB_NAME))
            db_name = Config.PROD_DB_NAME

        # Подключаемся к базе данных по умолчанию, чтобы создать нашу базу, если надо
        general_conn = psycopg2.connect("host='" + Config.DB_HOST + "' port=" + Config.DB_PORT +
            " dbname='postgres' user='" + Config.DB_USER + "' password='" + Config.DB_PASSWORD + "'")
        general_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = general_conn.cursor()
        sql = "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = '{}');".format(db_name)
        cur.execute(sql)
        is_db_exists = bool(cur.fetchone()[0])
        if not is_db_exists:  # Если база данных ещё не создана
            sql = "CREATE DATABASE {};".format(db_name)
            Logger.print(str(sql))
            cur.execute(sql)
        else:
            Logger.print("База {} уже существует, пропускаем этап создания.".format(db_name))
        general_conn.close()


        Logger.print("\n\n===================================================")
        Logger.print("Создаём таблицы:")

        def create_table(table_name: str, description: str):
            Logger.print("\n" + description)
            sql = "SELECT EXISTS(SELECT 1 FROM pg_class tbl WHERE tbl.relname = '{}');".format(table_name)
            is_table_exists = bool(DbListItemsIterator("init_db", sql).fetchone()[0])
            if not is_table_exists:
                DbExecuteNonQuery.execute_file(
                    "init_db",
                    os.path.join("init_db", "tables", "{}.sql".format(table_name))
                )
            else:
                Logger.print("Таблица {} уже существует, пропускаем этап создания.".format(table_name))

        def run_script(script_directory: str, script_name: str, description: str = None):
            Logger.print("Миграция {}...".format(script_name) if description is None else description)
            DbExecuteNonQuery.execute_file(
                "init_db",
                os.path.join("init_db", script_directory, "{}.sql".format(script_name))
            )

        # Таблица со списком
        create_table("list", "Таблица со списком")
        run_script("tables", "list_MIGRATE")
        run_script("tables", "list_MIGRATE_is_deleted")
        run_script("tables", "list_MIGRATE_synonyms")

        # Таблица с рангами
        create_table("ranks", "Таблица с рангами")

        # Таблица с языками
        create_table("known_languages", "Таблица с языками")
        run_script("tables", "known_languages_MIGRATE")
        run_script("tables", "known_languages_MIGRATE_2")

        # Таблица с советами дня
        create_table("tips_of_the_day", "Таблица с советами дня")
        run_script("tables", "tips_of_the_day_ADD_page_url")

        # Таблица с запущенными задачами
        create_table("tasks", "Таблица с запущенными задачами")

        # Таблица с админ-пользователями
        create_table("admin_users", "Таблица с админ-пользователями")

        # Таблица с админ-пользователями
        create_table("changed_tips", "Таблица с изменениями советов")

        # Таблица с кешем запросов к дереву
        create_table("get_tree_cache", "Таблица с кешем запросов к дереву")

        # Заполняем данными
        Logger.print("\n\n===================================================")
        Logger.print("Заполняем данными:")
        if is_test:
            run_script("fill_tables", "list_TEST", "Таблица public.list (для теста)")
            run_script("fill_tables", "ranks_TEST", "Таблица public.ranks (для теста)")

        run_script("fill_tables", "known_languages_ANY", "Таблица public.known_languages (для прода/теста)")
        run_script("fill_tables", "known_languages_ANY_set_main", "Таблица public.known_languages (для прода/теста) - выбор основного языка для администрирования")
        if is_test:
            run_script("fill_tables", "tips_of_the_day_TEST", "Таблица public.tips_of_the_day (для теста)")
        else:
            run_script("fill_tables", "tips_of_the_day_PROD", "Таблица public.tips_of_the_day (для прода)")

        # Хранимки для выдачи данных
        # (триггерные функции надо писать в скрипте создания их таблицы)
        Logger.print("\n\n===================================================")
        Logger.print("Хранимки и прочие скрипты:")
        run_script("functions", "get_translations", "Хранимка по выдаче перевода...")
        run_script("functions", "get_tree_default", "Хранимка для выдачи дерева по умолчанию: перенакатываем...")
        run_script("functions", "get_tree_by_id", "Хранимка для выдачи дерева по id: перенакатываем...")
        run_script("functions", "get_childes_by_id", "Хранимка для подгрузки потомков дерева по id: перенакатываем...")
        run_script("functions", "get_favorites", "Хранимка по выдаче избранного: перенакатываем...")
        run_script("functions", "search_by_words", "Хранимка по поиску: перенакатываем...")
        run_script("functions", "get_tip_of_the_day", "Хранимка по выдаче совета дня...")
        run_script("functions", "get_tip_of_the_day_by_id", "Хранимка по выдаче совета дня по id...")
        run_script("functions", "service_update_leaves_count", "Хранимка по подсчёту листов в дереве: перенакатываем...")
        run_script("functions", "check_rights", "Хранимка по проверке прав пользователей-админов: перенакатываем...")
        run_script("functions", "percent_of", "Хранимка по расчёту процента от двух чисел (служебная): перенакатываем...")
        run_script("functions", "percent_of_to_color", "Хранимка по расчёту цвета от двух чисел (служебная): перенакатываем...")
        run_script("functions", "get_filling_stats", "Хранимка по выдаче статистики заполнения таблицы животных парсером: перенакатываем...")
        run_script("functions", "get_all_tips_translations", "Хранимка по выдаче советов для перевода: перенакатываем...")

        # Просто так
        Logger.print("\n\n===================================================")
        Logger.print("Миграция базы данных завершена.\nНаличие ошибок смотрите по префиксу $$$ выше.")
        sql = "SELECT COUNT(1) FROM public.list;"
        list_records_count = DbListItemsIterator("init_db", sql).fetchone()[0]
        Logger.print("В таблице public.list сейчас {} записей.".format(list_records_count))

        Logger.print("\n\n===================================================")
        Logger.print("\n\n")

    @staticmethod
    def add_list_item(title: str, page_id: str):
        # Добавляем новый элемент в список или обновляем уже существующий
        sql = """
                INSERT INTO public.list (title, page_id)
                  VALUES ({}, {})
                ON CONFLICT ON CONSTRAINT uq_list_page_id 
                  DO UPDATE 
                  SET synonyms = CASE WHEN list.synonyms IS NULL THEN ARRAY [list.title, EXCLUDED.title]
                                    ELSE array_append(list.synonyms, EXCLUDED.title)
                                 END;
            """.format(quote_string(title), quote_string(page_id))
        DbExecuteNonQuery.execute(DbFunctions.default_conn_tag, sql)

    @staticmethod
    def add_details_to_item(title, page_id, _type, image_url, wikipedias_by_languages, titles_by_languages, parent_title):
        # Добавляем новый элемент в список или обновляем уже существующий
        sql = """
                UPDATE public.list
                SET
                  title = '{}'
                  , type = '{}'
                  , image_url = '{}'
                  , wikipedias_by_languages = '{}'
                  , titles_by_languages = '{}'
                  , parent_title = '{}'
                WHERE page_id = '{}';
            """.format(
                str(title)
                , str(_type)
                , str(image_url)
                , json.dumps(wikipedias_by_languages)
                , json.dumps(titles_by_languages)
                , str(parent_title)
                , str(page_id)
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


def quote_nullable(val):
    if val is None:
        return "null"
    else:
        return "'" + str(val).replace("'", "''") + "'"

def quote_string(val):
    return "'" + str(val).replace("'", "''") + "'"
