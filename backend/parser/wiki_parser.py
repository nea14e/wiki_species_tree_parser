# -*- coding: utf-8 -*-
import json
import re
import sys
import traceback

from multiprocessing.queues import Queue

from requests import Session
from requests.utils import requote_uri
from bs4 import BeautifulSoup
import time

from parser.exceptions.code_must_be_fixed_exception import CodeMustBeFixedException
from parser.exceptions.must_be_skipped_exception import MustBeSkippedException
from parser.exceptions.wiki_api_exception import WikiApiException
from .db_functions import DbFunctions, DbListItemsIterator, DbExecuteNonQuery, quote_nullable, quote_string

from config import Config
from .logger import Logger


class MyRequests:
    session = None

    @classmethod
    def get_session(cls):
        if cls.session is None:
            cls.session = Session()
            cls.session.headers.update({
                "User-Agent": Config.WIKI_USER_AGENT
            })
        return cls.session


def main_from_web(args: str, log_query: Queue):
    Logger.log_query = log_query
    args = args.split(Config.PARSER_ARGS_DELIMITER)
    args = [arg.strip('"') for arg in args]
    Logger.print("PARSER PROCESS STARTED: args:", *args)
    sys.argv = args
    try:
        main()
    except:
        error_message = traceback.format_exc()
        for line in error_message.split("\n"):
            Logger.print(Config.LOGS_ERROR_PREFIX + line)


def main():
    if len(sys.argv) < 3:
        print_usage()
        return

    # is_test = sys.argv[1] == "test"

    stage_number = str(sys.argv[2])

    # Выберите нужное и подставьте сюда перед запуском
    if stage_number == '0':
        DbFunctions.init_db()
        return
    elif stage_number == 'test_task':  # Task to test tasks progress engine
        if len(sys.argv) >= 4:
            will_success = sys.argv[3] == "True"
        else:
            will_success = True
        if len(sys.argv) >= 5:
            timeout = float(sys.argv[4])
        else:
            timeout = 30.0
        test_task(timeout, will_success)
        return

    def apply_proxy(proxy_string: str):
        MyRequests.get_session().proxies = {"http": proxy_string, "https": proxy_string}

    # init_session()  # нужно только для РуВики. С Википедии можно скачивать данные без логина

    if stage_number == '1':
        if len(sys.argv) >= 4:
            list_page_title = sys.argv[3]
        else:
            list_page_title = "Категория:Животные_по_алфавиту"
        if len(sys.argv) >= 5:
            apply_proxy(str(sys.argv[5]))
        populate_list(list_page_title)  # 1 этап
    elif stage_number == '2':
        if len(sys.argv) >= 4:
            if sys.argv[3] == "True":
                skip_parsed_interval = True
            elif sys.argv[3] == "False":
                skip_parsed_interval = False
            else:
                raise ValueError("Не удаётся прочитать bool: " + str(sys.argv[3]))
        else:
            skip_parsed_interval = True
        if len(sys.argv) >= 5:
            where = sys.argv[4]
        else:
            where = ""
        if len(sys.argv) >= 6:
            apply_proxy(str(sys.argv[5]))
        parse_details(skip_parsed_interval, where)  # 2 этап
    elif stage_number == '3':
        if len(sys.argv) >= 4:
            where = sys.argv[3]
        else:
            where = ""
        correct_parents(where)  # 3 этап
    elif stage_number == '4':
        DbFunctions.update_leaves_count()
    else:
        print_usage()


def print_usage():
    Logger.print("Запускайте через параметры командной строки")
    Logger.print("Для 0 этапа - инициализации базы:")
    Logger.print("python3.6 wiki_parser.py 0 [\"test\" для тестового наполнения]")
    Logger.print("Для 1 этапа - составления списка:")
    Logger.print("python3.6 wiki_parser.py 1 [list_page_title] [from_title] [proxy_string]")
    Logger.print("Для 2 этапа - получения деталей по списку:")
    Logger.print("python3.6 wiki_parser.py 2 [\"True\" - начать от последнего распарсенного (по умолчанию) / \"False\"] [where_фильтр_на_список_как_в_SQL] [proxy_string]")
    Logger.print("Для 3 этапа - построения древовидной структуры:")
    Logger.print("python3.6 wiki_parser.py 3 [where_фильтр_на_список_как_в_SQL]")
    Logger.print("Для 4 этапа - подсчёта количества видов в каждом узле дерева:")
    Logger.print("python3.6 wiki_parser.py 4")
    Logger.print()
    Logger.print("Где proxy_string = \"протокол://адрес:порт@логин:пароль\" или \"протокол://адрес:порт\"")


def init_session():
    Logger.print("ИНИЦИАЛИЗАЦИЯ СЕССИИ...")

    # 1. Получаем логин-токен
    # 403 - Forbidden
    # response = MyRequests.get_session().get(
    #     Config.API_URL,
    #     params={
    #         "action": "query",
    #         "meta": "tokens",
    #         "type": "login",
    #         "format": "json"
    #     }
    # )
    # response.raise_for_status()
    # data = response.json()
    # if "error" in data:
    #     raise WikiApiException("Ошибка API при получении токена", data['error'])
    # login_token = data["query"]["tokens"]["logintoken"]
    # print("Логин-токен получен:", login_token)

    # 2. Логинимся (используя логин и пароль от аккаунта бота)
    response = MyRequests.get_session().post(
        Config.API_URL,
        data={
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "lgname": Config.WIKI_USER_NAME,
            "lgpassword": Config.WIKI_USER_PASSWORD,
            # "lgtoken": login_token,
            "format": "json"
        }
    )
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise WikiApiException("Ошибка API при залогинивании", data['error'])

    # 3. Узнаём текущие лимиты запросов API
    response = MyRequests.get_session().post(
        Config.API_URL,
        data={
            "action": "query",
            "meta": "userinfo",
            "uiprop": "ratelimits",
            "format": "json",
        }
    )
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise WikiApiException("Ошибка API при залогинивании", data['error'])
    user_info = json.dumps(data["query"]["userinfo"])
    Logger.print("Действующие лимиты API:\n", user_info)

    Logger.print("СЕССИЯ УСПЕШНО ПРОИНИЦИАЛИЗИРОВАНА")


def populate_list(list_page_title: str):
    Logger.print("ЗАПУЩЕН 1 ЭТАП - СОСТАВЛЕНИЕ СПИСКА. Название списка: '{}'."
                 .format(list_page_title))

    query_params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Категория:Животные по алфавиту",
        "cmlimit": "500",  # максимум 500 (или 5000 с флагом бота)
        "format": "json",
        "cmtype": "page",  # только статьи (не подкатегории и не файлы)
        "continue": ""  # обязательно для постраничной выдачи
    }

    succeeds = 0
    skipped = 0
    errors = 0
    cmcontinue = None
    while True:  # Цикл перехода на след. страницу
        if cmcontinue is not None:
            query_params["cmcontinue"] = cmcontinue
        response = MyRequests.get_session().post(Config.API_URL, data=query_params)
        if response.status_code == 429:
            print("Лимит запросов превышен!")
            retry_after = int(response.headers.get("Retry-After"))
            print(f"Ждать: {retry_after} сек")
            time.sleep(retry_after + Config.TOO_MANY_REQUESTS_ADDITIONAL_DELAY)
        data = response.json()
        if "error" in data:
            raise WikiApiException("Ошибка API на этапе 1:\n" + json.dumps(data['error']))
        response.raise_for_status()
        cmcontinue = data["continue"]["cmcontinue"] if "continue" in data and "cmcontinue" in data["continue"] else None
        list_data = data["query"]["categorymembers"]

        # Сохраняем в базу ссылки, чтобы потом по ним переходить
        for item in list_data:
            try:
                item_page_id = str(item["pageid"])
                item_title = item["title"]

                query = """
                    INSERT INTO public.list (title, page_id)
                      VALUES ({}, {})
                    ON CONFLICT ON CONSTRAINT uq_list_page_id 
                      DO NOTHING;
                """.format(
                    quote_string(item_title),
                    quote_string(item_page_id)
                )
                DbExecuteNonQuery.execute('populate_list', query)

                succeeds += 1
            except BaseException:
                errors += 1
                Logger.print('Ошибка:\n', traceback.format_exc())

        if cmcontinue is not None:
            Logger.print("Страница обработана. Следующая - {}. Всего успешно {} элементов, {} пропущено, {} ошибок."
                         .format(cmcontinue, succeeds, skipped, errors)
            )
            time.sleep(Config.NEXT_LIST_PAGE_DELAY)
        else:
            Logger.print(
                "ВЕСЬ СПИСОК СОСТАВЛЕН! Всего успешно {} элементов, {} пропущено, {} ошибок."
                .format(succeeds, skipped, errors)
            )
            return


def parse_details(skip_parsed_interval, where=""):
    lang_key = "ru"

    query = """
      SELECT l.id,
             l.title,
             l.page_id,
             (SELECT array_agg(s.title)
              FROM public.synonyms s
              WHERE s.lang_key = {}
                AND s.list_id = l.id) AS synonyms
      FROM public.list l
      WHERE l.type IS NULL
            AND is_deleted = false
      """.format(quote_string(lang_key))
    if skip_parsed_interval:
        query += """
            AND title > (SELECT COALESCE(MAX(title), '')
                      FROM public.list
                      WHERE type IS NOT NULL
            """
        if where is not None and where != "":
            query += """
                        AND {}
            """.format(where)
        query += ")"
    if where is not None and where != "":
        query += """
        AND {}
        """.format(where)
    query += """
      ORDER BY title;
    """
    Logger.print("Список для парсинга:\n" + query)
    list_iterator = DbListItemsIterator("parse_details:list_to_parse", query)

    # Цикл по элементам из списка, подготовленного с помощью populate_list()
    item_counter = 0
    skipped_counter = 0
    without_parents = 0
    errors = 0
    while True:
        list_item = list_iterator.fetchone()
        if not list_item:
            break
        try:
            details = ListItemDetails(id=list_item[0], title=list_item[1], page_id=list_item[2], synonyms=list_item[3])
            if details.synonyms is None:
                details.synonyms = []
            Logger.print('===========================================')
            Logger.print(f"ПОЛУЧАЕМ ДЕТАЛИ О: id: {details.id} title: {details.title} page_id: {details.page_id}")

            # Получение wikitext по page_id:
            # query_params = {
            #     "action": "query",
            #     "format": "json",
            #     "prop": "info|revisions",
            #     "inprop": "title",  # TODO оптимизировать запрос
            #     "rvprop": "content",
            #     "pageids": details.page_id,
            #     "rvslots": "main"
            # }
            # Получение wikitext по title
            # query_params = {
            #     "action": "query",
            #     "format": "json",
            #     "prop": "revisions",
            #     "rvprop": "content",
            #     "titles": "Панда",
            #     "redirects": 1,
            #     "rvslots": "main"
            # }
            # response = MyRequests.get_session().get(Config.API_URL, params=query_params)
            # response.raise_for_status()
            # data = response.json()
            # if "error" in data:
            #     raise WikiApiException("Ошибка API на стадии 2", data['error'])
            # pages = data.get("query", {}).get("pages", {})
            # # В ответе ключ — это page_id (или -1, если не найдено)
            # page_info = next(iter(pages.values()), None)
            # page_wikitext = page_info["revisions"][0]["slots"]["main"]["*"]


            # Получение html по title
            query_params = {
                "action": "parse",
                "format": "json",
                "prop": "text",
                "page": details.title,
                "redirects": 1
            }
            response = MyRequests.get_session().get(Config.API_URL, params=query_params)
            if response.status_code == 429:
                print("Лимит запросов превышен!")
                retry_after = int(response.headers.get("Retry-After"))
                print(f"Ждать: {retry_after} сек")
                time.sleep(retry_after + Config.TOO_MANY_REQUESTS_ADDITIONAL_DELAY)
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                raise WikiApiException("Ошибка API на стадии 2", data['error'])
            parse = data["parse"]
            if details.title not in details.synonyms:
                details.synonyms.append(details.title)
            if parse["title"] not in details.synonyms:
                details.synonyms.append(parse["title"])
            html = parse["text"]["*"]
            soup = BeautifulSoup(html, "html.parser")

            details = parse_levels(soup, details)
            details = parse_image(soup, details)
            details = parse_wikipedias_hrefs(soup, details)

            query = """
              UPDATE public.list
              SET title = {}
                , type = {}
                , image_url = {}
                , parent_title = {}
                , parent_type = {}
                , wikipedias_by_languages = {}
                , titles_by_languages = {}
                , last_error_message = NULL
              WHERE id = {};
            """.format(
                quote_string(details.title)
                , quote_string(details.type)
                , quote_nullable(details.image_url)
                , quote_nullable(details.parent_title)
                , quote_nullable(details.parent_type)
                , quote_string(json.dumps(details.wikipedias_by_languages))
                , quote_string(json.dumps(details.titles_by_languages))
                , quote_string(details.id)
            )
            DbExecuteNonQuery.execute('parse_details:update_details', query)

            for synonym in details.synonyms:
                query = """
                    INSERT INTO public.synonyms(lang_key, list_id, title)
                    VALUES ({}, {}, {})
                    ON CONFLICT
                        ON CONSTRAINT pk_synonyms
                            DO NOTHING;
                """.format(
                    quote_string(lang_key),
                    int(details.id),
                    quote_string(synonym)
                )
                DbExecuteNonQuery.execute('parse_details:update_details', query)

            item_counter += 1

        except MustBeSkippedException as e:
            Logger.print(e.message)
            skipped_counter += 1
            query = """
                          UPDATE public.list
                          SET last_error_message = {},
                              is_deleted = true
                          WHERE id = {};
                        """.format(
                quote_string(e.message)
                , quote_string(str(list_item[0]))
            )
            DbExecuteNonQuery.execute('parse_details:update_details', query)

        except BaseException as e:
            err_message = "Stage 2 error:\n" + traceback.format_exc()
            Logger.print('Ошибка:\n', err_message)
            query = """
              UPDATE public.list
              SET last_error_message = {}
              WHERE id = {};
            """.format(
                quote_string(err_message)
                , quote_string(str(list_item[0]))
            )
            DbExecuteNonQuery.execute('parse_details:update_details', query)
            errors += 1

        time.sleep(Config.NEXT_DETAILS_PAGE_DELAY)
    Logger.print("\n")
    Logger.print("ПАРСИНГ ДЕТАЛЕЙ ЗАДАННЫХ ВИДОВ ОКОНЧЕН!")
    Logger.print(f"Добавлены детали о {item_counter} элементов.")
    Logger.print(f"Пропущено {skipped_counter} ненужных элементов.")
    Logger.print(f"Не найдены родители для {without_parents} элементов.")
    Logger.print(f"Ошибки для {errors} элементов.")


class ListItemDetails:
    def __init__(self, id, title, page_id, synonyms):
        self.id = id
        self.title = title
        self.page_id = page_id
        self.type = None
        self.image_url = None
        self.parent_title = None
        self.parent_type = None
        self.wikipedias_by_languages = {}
        self.titles_by_languages = {}
        self.synonyms = synonyms


def parse_levels(soup, details: ListItemDetails):
    # Side panel
    infobox = soup.select_one(".infobox")

    if "Устаревшее таксономическое" in infobox.text:
        raise MustBeSkippedException("Таксон устарел и должен быть пропущен")

    # Hierarchy levels (for example, Genus: †Avaceratops, Species: †A. lammersi)
    levels = list(infobox.select(".ts-Taxonomy-rang-row"))
    if not levels:
        levels_table = infobox.select_one("tbody > tr:nth-of-type(4) > td > table")
        if levels_table:
            levels = list(levels_table.select("tr"))
        else:
            levels_table = infobox.select_one("tbody > tr:nth-of-type(3) > td > table")
            if levels_table:
                levels = list(levels_table.select("tr"))
            else:
                raise CodeMustBeFixedException("Не удалось найти таблицу с иерархией.")
    levels = list(reversed(levels))

    if not levels:
        raise CodeMustBeFixedException("Найденная таблица с иерархией пуста.")

    # Parse one level:
    def get_level_info(level):
        # Searching for elements:
        if level.name == "div":
            level_type_el = level.select_one(".ts-Taxonomy-rang-label")
            level_title_el = level.select_one(".ts-Taxonomy-rang-name")
        elif level.name == "tr":
            level_type_el = level.select_one("th")
            level_title_el = level.select_one("td")
        else:
            raise CodeMustBeFixedException(f"Неизвестный тип уровня иерархии: level.name = '{level.name}'")

        b_el = level_title_el.select_one("b")
        a_href_el = level_title_el.select_one("a")

        # Extracting data from elements:
        level_type = (level_type_el
                      .text
                      .replace(" ", "")
                      .replace("\n", "")
                      .replace("\u00A0", "")
                      .replace(":", ""))
        level_title = ((b_el if b_el else a_href_el if a_href_el else level_title_el)
                       .text
                       .replace("†", "")
                       .replace("\u00A0", ""))
        if "," in level_title:
            level_title = level_title.split(",")[0]
        can_be_current_level = bool(b_el is not None and a_href_el is None)
        return level_type, level_title, can_be_current_level

    current_level = levels[0]
    level_0_type, level_0_title, can_be_current_level = get_level_info(current_level)
    if can_be_current_level:
        details.type = level_0_type
        if level_0_title not in details.synonyms:
            details.synonyms.append(level_0_title)
        if len(levels) > 1:
            parent_level = levels[1]
            details.parent_type, details.parent_title, _ = get_level_info(parent_level)
    else:
        details.parent_type = level_0_type
        details.parent_title = level_0_title

    Logger.print(f"Детали: {details.type} {details.title}, родитель: {details.parent_type} {details.parent_title}")
    return details


def parse_image(soup, details: ListItemDetails):
    images = soup.select(".infobox .infobox-image img")
    for img in images:
        if img is not None:
            if img.get("alt", None) != "edit":  # не картинка карандаша
                src = img.get('src', None)
                if src is not None:
                    Logger.print("Картинка: " + str(src))
                    details.image_url = src
                    return details
    # Картинки может не быть - всё равно обрабатывать эту страницу дальше
    Logger.print("Картинка НЕ НАЙДЕНА")
    return details


def parse_wikipedias_hrefs(soup, details: ListItemDetails):
    params = {
        "action": "query",
        "format": "json",
        "titles": details.title,
        "prop": "langlinks",
        "lllimit": "500"  # максимум ссылок в одном ответе
    }
    response = MyRequests.get_session().get(Config.API_URL, params=params)
    if response.status_code == 429:
        print("Лимит запросов превышен!")
        retry_after = int(response.headers.get("Retry-After"))
        print(f"Ждать: {retry_after} сек")
        time.sleep(retry_after + Config.TOO_MANY_REQUESTS_ADDITIONAL_DELAY)
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise WikiApiException("Ошибка API на стадии 2 Языки:\n", data['error'])

    pages = data["query"]["pages"]
    # В pages один ключ — id страницы; если страница не найдена, там будет ключ "-1"
    page_id = next(iter(pages))
    if page_id == "-1":
        return {}  # страница не существует

    lang_links = pages[page_id].get("langlinks", [])
    details.titles_by_languages = {ll["lang"]: ll["*"] for ll in lang_links}
    details.wikipedias_by_languages = {ll["lang"]: Config.WIKIPEDIAS_URL_MASK.format(ll["lang"], ll["*"])
                                       for ll in lang_links}
    Logger.print(f"Найдено {len(lang_links)} языков")
    return details


def correct_parents(where: str = None):
    """
    После парсинга списка пройдёмся по базе и заполним parent_id по parent_title.
    """
    Logger.print("Поправляем ссылки на родителей (построение дерева)...")
    query = """
        SELECT id, parent_title
        FROM public.list
        WHERE parent_title IS NOT NULL AND parent_id IS NULL  -- Только у которых уже заполнен текст родителя, но ещё не привязаны
    """
    if where is not None and where != "":
        query += " AND " + where
    query += ";"
    print(query)
    list_iterator = DbListItemsIterator('correct_parents:list', query)

    # Цикл по элементам из списка, подготовленного с помощью populate_list()
    success_counter = 0
    without_parents = 0
    total_counter = 0
    while True:
        list_item = list_iterator.fetchone()
        if not list_item:
            break
        cur_id = list_item[0]
        cur_parent_url = list_item[1]
        # Ищем родителя в базе по parent_title
        query = """
            SELECT id
            FROM public.list
            WHERE page_id = '{}'
            LIMIT 1;
        """.format(cur_parent_url)
        parent_in_db_iter = DbListItemsIterator('parse_details:get_parent', query)
        if parent_in_db_iter.rowcount() > 0:
            # Нашли в базе данных запись о родителе
            parent_in_db = parent_in_db_iter.fetchone()[0]
            query = """
              UPDATE public.list
              SET parent_id = '{}'
              WHERE id = '{}';
            """.format(parent_in_db, cur_id)
            DbExecuteNonQuery.execute('parse_details:set_parent_id', query)
            success_counter += 1
        else:
            # Не нашли
            without_parents += 1
        total_counter += 1
        if total_counter % 100 == 0:
            Logger.print("Построение дерева... найдено {}, не найдено {}, всего просмотрено {}"
                         .format(success_counter, without_parents, total_counter))
    Logger.print("\n")
    Logger.print("ОБНОВЛЕНИЕ РОДИТЕЛЕЙ ОКОНЧЕНО!")
    Logger.print("Добавлены родители к " + str(success_counter) + " элементам.")
    Logger.print("Не найдены родители для " + str(without_parents) + " элементов.")


def test_task(timeout: float, will_success: bool):
    Logger.print("Test task started for timeout = {0} seconds, will_success = {1}.".format(timeout, will_success))
    elapsed = 0
    while True:
        if timeout > 5:
            time.sleep(5)
            elapsed += 5
            timeout -= 5
            Logger.print("Test task is printing this to stdout every 5 seconds. Elapsed: {} seconds.".format(elapsed))
        else:
            time.sleep(timeout)
            elapsed += timeout
            if will_success:
                Logger.print("Test task is printing this to stdout WHEN COMPLETED at {} seconds.".format(elapsed))
                return
            else:
                Logger.print("Test task is printing this to stdout BEFORE ERROR at {} seconds.".format(elapsed))
                raise Exception("Test task raised this test exception!")


if __name__ == "__main__":
    main()
