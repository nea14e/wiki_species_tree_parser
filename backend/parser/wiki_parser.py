# -*- coding: utf-8 -*-
import json
import re
import sys
import traceback

# import requests
from multiprocessing.queues import Queue

from requests import Session
from requests.utils import requote_uri
from bs4 import BeautifulSoup
import time

from .db_functions import DbFunctions, DbListItemsIterator, DbExecuteNonQuery, quote_nullable, quote_string

from config import Config
from .logger import Logger


class MyRequests:
    session = None

    @classmethod
    def get_session(cls):
        if cls.session is None:
            cls.session = Session()
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

    is_test = sys.argv[1] == "test"

    stage_number = str(sys.argv[2])

    # Выберите нужное и подставьте сюда перед запуском
    if stage_number == '0':
        DbFunctions.init_db(is_test)
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

    DbFunctions.prepare_to_work(is_test=is_test)

    def apply_proxy(proxy_string: str):
        MyRequests.get_session().proxies = {"http": proxy_string, "https": proxy_string}

    if stage_number == '1':
        if len(sys.argv) >= 4:
            from_title = sys.argv[3]
        else:
            from_title = ""
        if len(sys.argv) >= 5:
            to_title = sys.argv[4]
        else:
            to_title = ""
        if len(sys.argv) >= 6:
            apply_proxy(str(sys.argv[5]))
        populate_list(from_title, to_title)  # 1 этап
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
    elif stage_number == 'parse_language':
        lang_key = str(sys.argv[3])
        if len(sys.argv) >= 5:
            if sys.argv[4] == "True":
                skip_parsed_interval = True
            elif sys.argv[4] == "False":
                skip_parsed_interval = False
            else:
                raise ValueError("Не удаётся прочитать bool: " + str(sys.argv[3]))
        else:
            skip_parsed_interval = True
        if len(sys.argv) >= 6:
            where = sys.argv[5]
        else:
            where = ""
        if len(sys.argv) >= 7:
            apply_proxy(str(sys.argv[6]))
        parse_language(lang_key, skip_parsed_interval, where)  # Добавление языка
    else:
        print_usage()


def print_usage():
    Logger.print("Запускайте через параметры командной строки")
    Logger.print("Для 0 этапа - инициализации базы:")
    Logger.print("python3.6 wiki_parser.py 0 [\"test\" для тестового наполнения]")
    Logger.print("Для 1 этапа - составления списка:")
    Logger.print("python3.6 wiki_parser.py 1 [from_title] [to_title] [proxy_string]")
    Logger.print("Для 2 этапа - получения деталей по списку:")
    Logger.print("python3.6 wiki_parser.py 2 [\"True\" - начать от последнего распарсенного (по умолчанию) / \"False\"] [where_фильтр_на_список_как_в_SQL] [proxy_string]")
    Logger.print("Для 3 этапа - построения древовидной структуры:")
    Logger.print("python3.6 wiki_parser.py 3 [where_фильтр_на_список_как_в_SQL]")
    Logger.print("Для 4 этапа - подсчёта количества видов в каждом узле дерева:")
    Logger.print("python3.6 wiki_parser.py 4")
    Logger.print("Отдельно - для получения перевода на язык по списку:")
    Logger.print("python3.6 wiki_parser.py parse_language <lang_key> [\"True\" - начать от последнего распарсенного (по умолчанию) / \"False\"] [where_фильтр_на_список_как_в_SQL] [proxy_string]")
    Logger.print()
    Logger.print("Где proxy_string = \"протокол://адрес:порт@логин:пароль\" или \"протокол://адрес:порт\"")


def populate_list(from_title: str = "", to_title: str = ""):
    Logger.print("ЗАПУЩЕН 1 ЭТАП - СОСТАВЛЕНИЕ СПИСКА. Ограничения: с '{}' по '{}'".format(from_title, to_title))

    url = "https://species.wikimedia.org/wiki/Special:AllPages"
    if from_title:
        url += "?from={}".format(requote_uri(from_title))
    if to_title:
        url += "&to={}".format(requote_uri(to_title))
    if from_title or to_title:
        url += "&namespace=0"

    html = MyRequests.get_session().get(url).content  # Парсим саму страницу
    wiki_html = BeautifulSoup(html, "html.parser")

    succeeds = 0
    skipped = 0
    errors = 0
    while True:  # Цикл перехода на след. страницу
        # Cсылка на следующую страницу
        navigate_page_elems = wiki_html.select("div.mw-allpages-nav > a")
        next_page_elem = None
        for el in navigate_page_elems:
            if "Next page" in el.text:
                next_page_elem = el
                break

        # Адрес из ссылки на следующую страницу
        if next_page_elem:
            next_page_url = next_page_elem["href"]
        else:
            next_page_url = None

        # Сохраем в базу ссылки, чтобы потом по ним переходить
        is_go_to_next_page = True
        for link in wiki_html.select("ul.mw-allpages-chunk > li > a"):
            try:
                item_title = link.text
                if to_title:
                    if item_title >= to_title:  # Дошли до верхей границы отрезка имён, заданного для выкачки
                        is_go_to_next_page = False
                        break
                if "." in item_title:  # Пропускаем имена учёных (с инициалами, поэтому у них точки)
                    skipped += 1
                    continue
                item_title = item_title.replace("'", "''")  # Экранирование для базы
                item_details_href = str(link["href"])
                if Config.URL_START_RELATIVE in item_details_href:
                    item_details_href = item_details_href[len(Config.URL_START_RELATIVE):]  # Ссылка (без начала)
                # Logger.print("Новый элемент в списке для парсинга: '%s', '%s'" % (item_title, item_details_href))  # debug only
                DbFunctions.add_list_item(item_title, item_details_href)
                succeeds += 1
            except BaseException:
                errors += 1
                Logger.print('Ошибка:\n', traceback.format_exc())

        if next_page_url and is_go_to_next_page:
            Logger.print("Страница обработана. Следующая - {}. Всего успешно {} элементов, {} пропущено, {} ошибок.".format(
                next_page_elem.text, succeeds, skipped, errors))
            html = MyRequests.get_session().get(Config.URL_DOMAIN.rstrip('/') + next_page_url).content  # Переходим на след страницу
            wiki_html = BeautifulSoup(html, "html.parser")
            time.sleep(Config.NEXT_PAGE_DELAY)
        else:
            Logger.print(
                "ВЕСЬ СПИСОК СОСТАВЛЕН! Всего успешно {} элементов, {} пропущено, {} ошибок.".format(succeeds, skipped,
                                                                                                     errors))
            return


def parse_details(skip_parsed_interval, where=""):
    query = """
      SELECT id, title, page_url
      FROM public.list
      WHERE type IS NULL
      """
    if skip_parsed_interval:
        query += """
            AND page_url > (SELECT COALESCE(MAX(page_url), '')
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
      ORDER BY page_url;
    """
    Logger.print("Список для парсинга:\n" + query)
    list_iterator = DbListItemsIterator("parse_details:list_to_parse", query)

    # Цикл по элементам из списка, подготовленного с помощью populate_list()
    item_counter = 0
    without_parents = 0
    errors = 0
    while True:
        list_item = list_iterator.fetchone()
        if not list_item:
            break
        try:
            details = ListItemDetails(id=list_item[0], title=list_item[1], page_url=list_item[2])
            url = Config.URL_START + details.page_url
            Logger.print('===========================================')
            Logger.print('ПОЛУЧАЕМ ДЕТАЛИ О: ' + details.title + " ссылка: " + url)
            html = MyRequests.get_session().get(url).content
            wiki_html = BeautifulSoup(html, "html.parser")

            # Парсинг информации
            all_content = wiki_html.select_one("div.mw-parser-output")
            details, err_message = parse_levels(all_content, details)
            if err_message:
                without_parents += 1
                DbExecuteNonQuery.execute('parse_details:update_details', "ROLLBACK;")
                query = """
                  UPDATE public.list
                  SET last_error_message = {}
                  WHERE id = {};
                """.format(
                    quote_string(err_message)
                    , quote_string(str(list_item[0]))
                )
                DbExecuteNonQuery.execute('parse_details:update_details', query)
                continue
            details = parse_image_wikispecies(all_content, details)
            details = parse_wikipedias_hrefs(wiki_html, details)

            # Запись всех подробностей в базу
            # (только если нашли родителя - без родителей в дереве элементы не нужны)
            query = """
              UPDATE public.list
              SET title = {}
                , type = {}
                , image_url = {}
                , parent_page_url = {}
                , wikipedias_by_languages = {}
                , titles_by_languages = {}
                , last_error_message = NULL
              WHERE id = {};
            """.format(
                quote_string(details.title)
                , quote_string(details.type)
                , quote_nullable(details.image_url)
                , quote_nullable(details.parent_page_url)
                , quote_string(json.dumps(details.wikipedias_by_languages))
                , quote_string(json.dumps(details.titles_by_languages))
                , quote_string(details.id)
            )
            DbExecuteNonQuery.execute('parse_details:update_details', query)
            item_counter += 1

        except:  # Ошибки базы могут разных видов. Ловим вообще все
            err_message = "Stage 2 error:\n" + traceback.format_exc()
            Logger.print('Ошибка:\n', err_message)
            DbExecuteNonQuery.execute('parse_details:update_details', "ROLLBACK;")
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

        time.sleep(Config.NEXT_PAGE_DELAY)
    Logger.print("\n")
    Logger.print("ПАРСИНГ ДЕТАЛЕЙ ЗАДАННЫХ ВИДОВ ОКОНЧЕН!")
    Logger.print("Добавлены детали о " + str(item_counter) + " элементов.")
    Logger.print("Не найдены родители для " + str(without_parents) + " элементов.")
    Logger.print("Ошибки для " + str(errors) + " элементов.")


class ListItemDetails:
    def __init__(self, id, title, page_url):
        self.id = id
        self.title = title
        self.page_url = page_url
        self.type = None
        self.image_url = None
        self.parent_page_url = None
        self.parent_title = None
        self.parent_type = None
        self.wikipedias_by_languages = {}
        self.titles_by_languages = {}


class MyException(BaseException):
    def __init__(self, message):
        self.message = message


def parse_image_wikispecies(main_content, details: ListItemDetails):
    images = main_content.select("figure img.mw-file-element")  # Перебираем все картинки справа в основном содержимом
    for img in images:
        if img is not None:
            if img.get("alt", None) != "edit":  # не картинка карандаша
                src = img['src']
                Logger.print("Картинка в Викивидах: " + str(src))
                details.image_url = src
                return details
    # Картинки может не быть - всё равно обрабатывать эту страницу дальше
    Logger.print("Картинка в Викивидах НЕ НАЙДЕНА")
    details.image_url = None
    return details


def parse_levels(tree_box, details: ListItemDetails):
    """
            Парсим таблицу элементов-родителей, в которые вложен данный элемент
            (для черепах это будет что-то вроде
              Царство: Животные, Тип: Хордовые, Подтип: Позвоночные, Класс: Пресмыкающиеся, Отряд: Черепахи)
            Вытаскивает: тип текущего элемента (Отряд),
              название и тип ближайшего имеющегося в базе родителя (Класс: Пресмыкающиеся)

    Например, для https://species.wikimedia.org/wiki/Aaptos
    в раскрывающейся таблице
    [
        'Superregnum: <a href="/wiki/Eukaryota" title="Eukaryota">Eukaryota</a>',
        ...
        'Ordo: <a href="/wiki/Suberitida" title="Suberitida">Suberitida</a> ',
        ''
    ]
    а вне таблицы содержатся
    [
        'Familia: <a href="/wiki/Suberitidae" title="Suberitidae">Suberitidae</a>',
        'Genus: <i><a href="/wiki/Aaptos" title="Aaptos">Aaptos</a></i>',     <--- предыдущий перед mw-selflink - родитель. Он может быть внутри таблицы.
        'Species: <i><a class="mw-selflink selflink">Aaptos rosacea</a></i>'  <--- mw-selflink указывает, что это текущий элемент, которому посвящена страница

    ]
    """


    levels_p = tree_box.find("p", recursive=False)
    levels = str(levels_p)[len("<p>"):-len("</p>")].replace("\n", "").split("<br/>")
    levels = [level.replace('<i>', '').replace('</i>', '') for level in levels]

    # Текущий уровень

    is_current_found = False
    current_level_ind = None
    for ind, level in enumerate(levels):
        matches = re.match(r"(.+?):.+?<a.+?mw-selflink.+?>(.+?)</a>.*", level, re.DOTALL)
        if matches is not None:
            # эта ссылка ЕСТЬ в просматриваемом нами уровне
            is_current_found = True
            current_level_ind = ind
            details.type = matches.group(1)  # текст до двоеточия
            details.title = matches.group(2)  # текст внутри <a>...</a>
            Logger.print("Текущий уровень: тип: {} название: {}".format(details.type, details.title))
            break

    # Если текущий уровень почему-то не найден
    if not is_current_found:
        Logger.print("Ошибка: текущий уровень не найден!")
        return details, "Stage 2 error: current level not found on this page."

    # Предыдущий уровень

    ind = current_level_ind - 1
    if ind >= 0:
        parent_level = levels[ind]
        matches = re.match(r"""(.+?):.+?<a.+?href="(.+?)".*?>(.+?)</a>.*""", parent_level, re.DOTALL)
        if matches is not None:
            details.parent_type = matches.group(1)
            details.parent_title = matches.group(3)
            href = matches.group(2)
            if href[:len("/wiki/")] == "/wiki/":
                details.parent_page_url = href[len("/wiki/"):]
            else:
                return details, "Stage 2 error: <a href> starts with unknown prefix instead of '/wiki/': href='{}'!" \
                    .format(href)
            Logger.print("Предыдущий уровень: основной: '{}': '{}', href='{}'".format(details.parent_type, details.parent_title, details.parent_page_url))
            return details, None
        else:
            Logger.print("Предыдущий уровень: основной: не найден!")
            return details, "Stage 2 error: previous level (main) not found on this page."
    else:
        levels_collapsible_p = tree_box.select_one("table:nth-child(2).wikitable.mw-collapsible > tbody > tr:nth-child(2) > td > p")
        levels_collapsible = str(levels_collapsible_p)[len("<p>"):-len("</p>")].replace("\n", "").split("<br/>")
        if len(levels_collapsible) >= 2:
            parent_level = levels_collapsible[-2]
            matches = re.match(r"""(.+?):.+?<a.+?href="(.+?)".*?>(.+?)</a>.*""", parent_level, re.DOTALL)
            if matches is not None:
                details.parent_type = matches.group(1)
                details.parent_title = matches.group(3)
                details.parent_page_url = matches.group(2)[len("/wiki/"):]
                Logger.print("Предыдущий уровень: в таблице: '{}': '{}', href='{}'".format(details.parent_type, details.parent_title, details.parent_page_url))
                return details, None
            else:
                Logger.print("Предыдущий уровень: в таблице: не найден!")
                return details, "Stage 2 error: previous level (in table) not found on this page."
        else:
            Logger.print("Предыдущий уровень: в таблице: не найден - уровней мало!")
            return details, "Stage 2 error: previous level (in table) not found on this page - levels too few."


def parse_wikipedias_hrefs(wiki_html, details: ListItemDetails):
    # Ссылки на Википедии разных языков
    a_s = wiki_html.select("#p-lang > div > ul > li > a")
    for a in a_s:
        if a.text != "":
            match = re.search(Config.WIKIPEDIAS_URL_MASK, a["href"])
            hreflang = match[1]
            href = match[2]
            details.wikipedias_by_languages[hreflang] = href
            if Config.IS_DEBUG:
                wikipedia_page_url = Config.WIKIPEDIA_URL_CONSTRUCTOR.format(hreflang, href)
                Logger.print("Найдена ссылка на Википедию: язык: {} ссылка: {}".format(hreflang, wikipedia_page_url))
    return details


def parse_language(lang_key: str, skip_parsed_interval: bool, where: str = ""):
    Logger.print("Парсим язык: {}, skip_parsed_interval = {}, where = \"{}\"".format(lang_key, skip_parsed_interval, where))
    query = """
      SELECT id, title, image_url, wikipedias_by_languages, titles_by_languages
      FROM public.list
      WHERE (wikipedias_by_languages ? {}) AND NOT(titles_by_languages ? {})
      """.format(quote_string(lang_key), quote_string(lang_key))
    if skip_parsed_interval:
        query += """
            AND page_url > (SELECT COALESCE(MAX(page_url), '')
                      FROM public.list
                      WHERE (titles_by_languages ? {})
            """.format(quote_string(lang_key), quote_string(lang_key))
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
      ORDER BY page_url;
    """
    Logger.print("Список для парсинга:\n" + query)
    list_iterator = DbListItemsIterator("parse_language:list_to_parse", query)

    # Цикл по элементам из списка, подготовленного с помощью populate_list()
    item_counter = 0
    added_images = 0
    errors = 0
    while True:
        list_item = list_iterator.fetchone()
        if not list_item:
            break
        try:
            cur_id = list_item[0]
            cur_title = list_item[1]
            cur_image_url = list_item[2]
            cur_wikipedias_by_languages = list_item[3]
            cur_titles_by_languages = list_item[4]

            # Заходим на саму страницу Википедии нужного языка,
            # т.к. переведённое название вида не содержится на Викивидах и поэтому надо заходить на Википедию
            wikipedia_page_url = Config.WIKIPEDIA_URL_CONSTRUCTOR.format(lang_key, cur_wikipedias_by_languages[lang_key])
            Logger.print("Парсим Википедию: язык: {}, название: {}, ссылка: {}".format(lang_key, cur_title, wikipedia_page_url))
            html = MyRequests.get_session().get(wikipedia_page_url).content
            wiki_html = BeautifulSoup(html, "html.parser")

            # Парсим перевод названия вида
            title_on_lang = wiki_html.select_one("#content > h1#firstHeading").text
            if Config.IS_DEBUG:
                Logger.print("...переведённое название: {}".format(title_on_lang))
            cur_titles_by_languages[lang_key] = title_on_lang

            # Парсим картинку, если её ещё не нашли ранее для текущего вида
            if cur_image_url is None:
                image = wiki_html.select_one(  # Картинка в карточке вида (при этом не карта распространения)
                    "#mw-content-text > div > table.infobox > tbody > tr:nth-child(2) img"
                )
                if image is not None:
                    if image.get("alt", None) != "edit" and image.get("alt", None) != "e":  # картинка карандаша
                        cur_image_url = str(image['src'])
                        Logger.print("...добавили картинку: {}".format(cur_image_url))
                        added_images += 1

            # Запись всех подробностей в базу
            # (только если нашли родителя - без родителей в дереве элементы не нужны)
            query = """
              UPDATE public.list
              SET image_url = {}
                , titles_by_languages = {}
                , last_error_message = NULL
              WHERE id = {};
            """.format(
                quote_nullable(cur_image_url)
                , quote_string(json.dumps(cur_titles_by_languages))
                , quote_string(cur_id)
            )
            DbExecuteNonQuery.execute('parse_language:update_details', query)
            item_counter += 1

        except:  # Ошибки базы могут разных видов. Ловим вообще все
            err_message = "Stage parse_language error:\n" + traceback.format_exc()
            Logger.print('Ошибка:\n', err_message)
            DbExecuteNonQuery.execute('parse_language:update_details', "ROLLBACK;")
            query = """
              UPDATE public.list
              SET last_error_message = {}
              WHERE id = {};
            """.format(
                quote_string(err_message)
                , quote_string(str(list_item[0]))
            )
            DbExecuteNonQuery.execute('parse_language:update_details', query)
            errors += 1

        time.sleep(Config.NEXT_PAGE_DELAY)
    Logger.print("\n")
    Logger.print("ПАРСИНГ ЯЗЫКА ЗАДАННЫХ ВИДОВ ОКОНЧЕН!")
    Logger.print("Добавлены переводы для " + str(item_counter) + " элементов.")
    Logger.print("Добавлены картинки для " + str(added_images) + " элементов.")
    Logger.print("Ошибки для " + str(errors) + " элементов.")


def correct_parents(where: str = None):
    """
    После парсинга списка пройдёмся по базе и заполним parent_id по parent_page_url.
    """
    Logger.print("Поправляем ссылки на родителей (построение дерева)...")
    query = """
        SELECT id, parent_page_url
        FROM public.list
        WHERE parent_page_url IS NOT NULL AND parent_id IS NULL  -- Только у которых уже заполнен текст родителя, но ещё не привязаны
    """
    if where is not None and where != "":
        query += " AND " + where
    query += ";"
    print(query)
    list_iterator = DbListItemsIterator('correct_parents:list', query)

    # Цикл по элементам из списка, подготовленного с помощью populate_list()
    item_counter = 0
    without_parents = 0
    while True:
        list_item = list_iterator.fetchone()
        if not list_item:
            break
        cur_id = list_item[0]
        cur_parent_url = list_item[1]
        # Ищем родителя в базе по parent_page_url
        query = """
            SELECT id
            FROM public.list
            WHERE page_url = '{}'
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
            item_counter += 1
        else:
            # Не нашли
            without_parents += 1
    Logger.print("\n")
    Logger.print("ОБНОВЛЕНИЕ РОДИТЕЛЕЙ ОКОНЧЕНО!")
    Logger.print("Добавлены родители к " + str(item_counter) + " элементам.")
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
