# -*- coding: utf-8 -*-
import json
import re
import sys
import traceback

# import requests
from requests import Session
from requests.utils import requote_uri
from bs4 import BeautifulSoup
import time

from db_functions import DbFunctions, DbListItemsIterator, DbExecuteNonQuery, quote_nullable, quote_string

from config import Config


class MyRequests:
    session = None

    @classmethod
    def get_session(cls):
        if cls.session is None:
            cls.session = Session()
        return cls.session


def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    stage_number = str(sys.argv[1])

    # Выберите нужное и подставьте сюда перед запуском
    if stage_number == '0':
        if len(sys.argv) >= 3:
            is_test = bool(str(sys.argv[2]).lower() == "test")
        else:
            is_test = False
        DbFunctions.init_db(is_test)
        return

    DbFunctions.init_db(is_test=False)

    def apply_proxy(proxy_string: str):
        MyRequests.get_session().proxies = {"http": proxy_string, "https": proxy_string}

    if stage_number == '1':
        if len(sys.argv) >= 3:
            from_title = sys.argv[2]
        else:
            from_title = ""
        if len(sys.argv) >= 4:
            to_title = sys.argv[3]
        else:
            to_title = ""
        if len(sys.argv) >= 5:
            apply_proxy(str(sys.argv[4]))
        populate_list(from_title, to_title)  # 1 этап
    elif stage_number == '2':
        if len(sys.argv) >= 3:
            if sys.argv[2] == "True":
                skip_parsed_interval = True
            elif sys.argv[2] == "False":
                skip_parsed_interval = False
            else:
                raise ValueError("Не удаётся прочитать bool: " + str(sys.argv[2]))
        else:
            skip_parsed_interval = True
        if len(sys.argv) >= 4:
            where = sys.argv[3]
        else:
            where = ""
        if len(sys.argv) >= 5:
            apply_proxy(str(sys.argv[4]))
        parse_details(skip_parsed_interval, where)  # 2 этап
    elif stage_number == '3':
        if len(sys.argv) >= 3:
            where = sys.argv[2]
        else:
            where = ""
        correct_parents(where)  # 3 этап
    elif stage_number == '4':
        DbFunctions.update_leaves_count()
    else:
        print_usage()


def print_usage():
    print("Запускайте через параметры командной строки")
    print("Для 0 этапа - инициализации базы:")
    print("python3.6 wiki_parser.py 0 [\"test\" для тестового наполнения]")
    print("Для 1 этапа - составления списка:")
    print("python3.6 wiki_parser.py 1 [from_title] [to_title] [proxy_string]")
    print("Для 2 этапа - получения деталей по списку:")
    print("python3.6 wiki_parser.py 2 [\"True\" - начать от последнего распарсенного (по умолчанию) / \"False\"] [where_фильтр_на_список_как_в_SQL] [proxy_string]")
    print("Для 3 этапа - построения древовидной структуры:")
    print("python3.6 wiki_parser.py 3 [where_фильтр_на_список_как_в_SQL]")
    print("Для 4 этапа - подсчёта количества видов в каждом узле дерева:")
    print("python3.6 wiki_parser.py 4")
    print()
    print("Где proxy_string = \"протокол://адрес:порт@логин:пароль\" или \"протокол://адрес:порт\"")


def populate_list(from_title: str = "", to_title: str = ""):
    print("ЗАПУЩЕН 1 ЭТАП - СОСТАВЛЕНИЕ СПИСКА. Ограничения: с '{}' по '{}'".format(from_title, to_title))

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
                # print("Новый элемент в списке для парсинга: '%s', '%s'" % (item_title, item_details_href))  # debug only
                DbFunctions.add_list_item(item_title, item_details_href)
                succeeds += 1
            except BaseException:
                errors += 1
                print('Ошибка:\n', traceback.format_exc())

        if next_page_url and is_go_to_next_page:
            print("Страница обработана. Следующая - {}. Всего успешно {} элементов, {} пропущено, {} ошибок.".format(
                next_page_elem.text, succeeds, skipped, errors))
            html = MyRequests.get_session().get(Config.URL_DOMAIN.rstrip('/') + next_page_url).content  # Переходим на след страницу
            wiki_html = BeautifulSoup(html, "html.parser")
            time.sleep(Config.NEXT_PAGE_DELAY)
        else:
            print(
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
    print("Список для парсинга:\n" + query)
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
            print('===========================================')
            print('ПОЛУЧАЕМ ДЕТАЛИ О: ' + details.title + " ссылка: " + details.page_url)
            html = MyRequests.get_session().get(Config.URL_START + details.page_url).content
            wiki_html = BeautifulSoup(html, "html.parser")

            # Парсинг информации
            all_content = wiki_html.select_one("div.mw-parser-output")
            is_parent_found, details = parse_levels(all_content, details)
            if not is_parent_found:
                without_parents += 1
                continue
            details = parse_image_wikispecies(all_content, details)
            details = parse_wikipedias(wiki_html, details)

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
            print('Ошибка:\n', traceback.format_exc())
            DbExecuteNonQuery.execute('parse_details:update_details', "ROLLBACK;")
            errors += 1

        time.sleep(Config.NEXT_PAGE_DELAY)
    print("\n")
    print("ПАРСИНГ ДЕТАЛЕЙ ЗАДАННЫХ ВИДОВ ОКОНЧЕН!")
    print("Добавлены детали о " + str(item_counter) + " элементов.")
    print("Не найдены родители для " + str(without_parents) + " элементов.")
    print("Ошибки для " + str(errors) + " элементов.")


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


def parse_image_wikispecies(main_content, details: ListItemDetails):
    div = main_content.select_one("div.thumb.tright")
    if div is not None:
        images = div.select("img")  # Перебираем все картинки справа в основном содержимом
        for img in images:
            if img is not None:
                if img.get("alt", None) != "edit":  # не картинка карандаша
                    src = img['src']
                    print("Картинка в Викивидах: " + str(src))
                    details.image_url = src
                    return details
    # Картинки может не быть - всё равно обрабатывать эту страницу дальше
    print("Картинка в Викивидах НЕ НАЙДЕНА")
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
            print("Текущий уровень: тип: {} название: {}".format(details.type, details.title))
            break

    # Если текущий уровень почему-то не найден
    if not is_current_found:
        print("Ошибка: текущий уровень не найден!")
        return False, details

    # Предыдущий уровень

    ind = current_level_ind - 1
    if ind >= 0:
        parent_level = levels[ind]
        matches = re.match(r"""(.+?):.+?<a.+?href="(.+?)".*?>(.+?)</a>.*""", parent_level, re.DOTALL)
        if matches is not None:
            details.parent_type = matches.group(1)
            details.parent_title = matches.group(3)
            details.parent_page_url = matches.group(2)[len("/wiki/"):]
            print("Предыдущий уровень: основной: '{}': '{}', href='{}'".format(details.parent_type, details.parent_title, details.parent_page_url))
            return True, details
        else:
            print("Предыдущий уровень: основной: не найден!")
            return False, details
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
                print("Предыдущий уровень: в таблице: '{}': '{}', href='{}'".format(details.parent_type, details.parent_title, details.parent_page_url))
                return True, details
            else:
                print("Предыдущий уровень: в таблице: не найден!")
                return False, details
        else:
            print("Предыдущий уровень: в таблице: не найден - уровней мало!")
            return False, details


def parse_wikipedias(wiki_html, details: ListItemDetails):
    # Ссылки на Википедии разных языков
    a_s = wiki_html.select("#p-lang > div > ul > li > a")
    for a in a_s:
        if a.text != "":
            match = re.search(Config.WIKIPEDIAS_URL_MASK, a["href"])
            hreflang = match[1]
            href = match[2]
            details.wikipedias_by_languages[hreflang] = href
            wikipedia_page_url = Config.WIKIPEDIA_URL_CONSTRUCTOR.format(hreflang, href)
            if Config.IS_DEBUG:
                print("Найдена ссылка на Википедию: язык: {} ссылка: {}".format(hreflang, wikipedia_page_url))

            html = MyRequests.get_session().get(wikipedia_page_url).content  # Парсим саму страницу Википедии
            wiki_html = BeautifulSoup(html, "html.parser")
            details = parse_one_wikipedia(hreflang, wiki_html, details)
            if details.image_url is None:
                details = parse_image_wikipedia(hreflang, wiki_html, details)
    print("Найдены языки: {}".format(details.titles_by_languages.keys()))
    return details


def parse_one_wikipedia(hreflang, wiki_html, details: ListItemDetails):
    title = wiki_html.select_one("#content > h1#firstHeading").text
    if Config.IS_DEBUG:
        print("Парсим страницу Википедии: Язык: {} Заголовок: {}".format(hreflang, title))
    details.titles_by_languages[hreflang] = title
    return details


def parse_image_wikipedia(hreflang, wiki_html, details: ListItemDetails):
    image = wiki_html.select_one(
        "#mw-content-text > div > table.infobox > tbody > tr:nth-child(2) img"
    )
    # Картинка в карточке вида (при этом не карта распространения)
    if image is not None:
        if image.get("alt", None) == "edit" or image.get("alt", None) == "e":
            return details  # картинка карандаша
        src = str(image['src'])
        print("Картинка в Википедии: Язык: {} Картинка: {}".format(hreflang, src))
        details.image_url = src
    return details


def correct_parents(where: str = None):
    """
    После парсинга списка пройдёмся по базе и заполним parent_id по parent_page_url.
    """
    print("Поправляем ссылки на родителей (построение дерева)...")
    query = """
        SELECT id, parent_page_url
        FROM public.list
        WHERE parent_page_url IS NOT NULL AND parent_id IS NULL  -- Только у которых уже заполнен текст родителя, но ещё не привязаны
    """
    if where is not None and where != "":
        query += " AND " + where
    query += ";"
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
    print("\n")
    print("ОБНОВЛЕНИЕ РОДИТЕЛЕЙ ОКОНЧЕНО!")
    print("Добавлены родители к " + str(item_counter) + " элементам.")
    print("Не найдены родители для " + str(without_parents) + " элементов.")




if __name__ == "__main__":
    main()
