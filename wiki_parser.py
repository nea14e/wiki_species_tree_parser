# -*- coding: utf-8 -*-
import json
import re
import sys
import traceback

import requests
from requests.utils import requote_uri
from bs4 import BeautifulSoup
import time

from db_functions import DbFunctions, DbListItemsIterator, DbExecuteNonQuery, quote_nullable
# from db_functions_sqlite import DbFunctions, DbListItemsIterator, DbExecuteNonQuery, quote_nullable   # TODO перейти полностью на использование SQLite
import db_functions_sqlite

IS_DEBUG = False

NEXT_PAGE_DELAY = 0.2

# ! Внимание! Чтобы использовать Selenium, нужен Firefox версии не выше 66.
# Скачать его можно отсюда: https://ftp.mozilla.org/pub/firefox/releases/66.0.5/

URL_START = "https://species.wikimedia.org/wiki/"
WIKIPEDIAS_URL_MASK = r"https:\/\/(.+)\.wikipedia\.org\/wiki\/(.+)"
WIKIPEDIA_URL_CONSTRUCTOR = "https://{}.wikipedia.org/wiki/{}"


def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    stage_number = sys.argv[1]

    DbFunctions.init_db()

    # Выберите нужное и подставьте сюда перед запуском
    if stage_number == '0':
        pass  # Только инициализация базы (написана вне if)
    elif stage_number == '1':
        if len(sys.argv) >= 3:
            from_title = sys.argv[2]
        else:
            from_title = ""
        if len(sys.argv) >= 4:
            to_title = sys.argv[3]
        else:
            to_title = ""
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
        parse_details(skip_parsed_interval, where)  # 2 этап
    elif stage_number == '3':
        if len(sys.argv) >= 3:
            where = sys.argv[2]
        else:
            where = ""
        correct_parents(where)  # 3 этап
    elif stage_number == 'create_sqlite':
        db_functions_sqlite.DbFunctions.init_db()
    elif stage_number == 'copy_db_to_sqlite':
        if len(sys.argv) >= 3:
            where = sys.argv[2]
        else:
            where = ""
        copy_db_to_sqlite(where)
    else:
        print_usage()


def print_usage():
    print("ОШИБКА: неизвестные параметры.")
    print("Запускайте через параметры командной строки")
    print("Для 0 этапа - инициализации базы:")
    print("0")
    print("Для 1 этапа - составления списка:")
    print("1 from_title to_title")
    print("Для 2 этапа - получения деталей по списку:")
    print("2 [bool(True начать от последнего распарсенного)=True] [where_фильтр_на_список=\"\"]")
    print("Для 3 этапа - построения древовидной структуры:")
    print("3 [where_фильтр_на_список=\"\"]")


def populate_list(from_title: str = "", to_title: str = ""):
    print("ЗАПУЩЕН 1 ЭТАП - СОСТАВЛЕНИЕ СПИСКА. Ограничения: с '{}' по '{}'".format(from_title, to_title))

    html = requests.get(
        "https://species.wikimedia.org/wiki/Special:AllPages?from={}&to={}&namespace=0" \
            .format(requote_uri(from_title), requote_uri(to_title))
    ).content  # Парсим саму страницу Википедии
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
        for link in wiki_html.select("ul.mw-allpages-chunk > li > a"):
            try:
                item_title = link.text
                if "." in item_title:  # Пропускаем имена учёных (с инициалами, поэтому у них точки)
                    skipped += 1
                    continue
                item_title = item_title.replace("'", "''")  # Экранирование для базы
                item_details_href = str(link["href"])
                item_details_href = item_details_href[len(URL_START):]  # Ссылка (без начала)
                # print("Новый элемент в списке для парсинга: '%s', '%s'" % (item_title, item_details_href))  # debug only
                DbFunctions.add_list_item(item_title, item_details_href)
                succeeds += 1
            except BaseException:
                errors += 1
                print('Ошибка:\n', traceback.format_exc())

        if next_page_url:
            print("Страница обработана. Следующая - {}. Всего успешно {} элементов, {} пропущено, {} ошибок.".format(
                next_page_elem.text, succeeds, skipped, errors))
            html = requests.get(next_page_url).content  # Переходим на след страницу
            wiki_html = BeautifulSoup(html, "html.parser")
            time.sleep(NEXT_PAGE_DELAY)
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
            details = ListItemDetails(list_item[0], list_item[1], list_item[2])
            print('===========================================')
            print('ПОЛУЧАЕМ ДЕТАЛИ О: ' + details.title + " ссылка: " + details.page_url)
            html = requests.get(URL_START + details.page_url).content
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
              SET title = '{}'
                , type = '{}'
                , image_url = {}
                , parent_page_url = {}
                , wikipedias_by_languages = '{}'
                , titles_by_languages = '{}'
              WHERE id = '{}';
            """.format(
                str(details.title)
                , str(details.type)
                , quote_nullable(details.image_url)
                , quote_nullable(details.parent_page_url)
                , json.dumps(details.wikipedias_by_languages)
                , json.dumps(details.titles_by_languages)
                , str(details.id)
            )
            DbExecuteNonQuery.execute('parse_details:update_details', query)
            item_counter += 1

        # except WebDriverException:  TODO
        #     print('Ошибка:\n', traceback.format_exc())
        #     errors += 1
        except:  # Ошибки базы могут разных видов. Ловим вообще все
            print('Ошибка:\n', traceback.format_exc())
            DbExecuteNonQuery.execute('parse_details:update_details', "ROLLBACK;")
            errors += 1

        time.sleep(NEXT_PAGE_DELAY)
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
        image = div.select_one("img")  # Просто любая картинка справа в основном содержимом
        src = image['src']
        print("Картинка в Викивидах: " + str(src))
        details.image_url = src
    else:  # Картинки может не быть - всё равно обрабатывать эту страницу дальше
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


    levels_p = tree_box.select_one("p:nth-child(3)")
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
    a_s = wiki_html.select("div#p-lang > div > ul > li > a")
    for a in a_s:
        if a.text != "":
            match = re.search(WIKIPEDIAS_URL_MASK, a["href"])
            hreflang = match[1]
            href = match[2]
            if IS_DEBUG:
                print("Ссылка на Википедию: язык: {} ссылка: {}".format(hreflang, href))
            details.wikipedias_by_languages[hreflang] = href
            wikipedia_page_url = WIKIPEDIA_URL_CONSTRUCTOR.format(hreflang, href)

            html = requests.get(wikipedia_page_url).content  # Парсим саму страницу Википедии
            wiki_html = BeautifulSoup(html, "html.parser")
            details = parse_one_wikipedia(hreflang, wiki_html, details)
            if details.image_url is None:
                details = parse_image_wikipedia(hreflang, wiki_html, details)
    return details


def parse_one_wikipedia(hreflang, wiki_html, details: ListItemDetails):
    title = wiki_html.select_one("div#content > h1").text
    if IS_DEBUG:
        print("Ссылка на Википедию: Язык: {} Заголовок: {}".format(hreflang, title))
    details.titles_by_languages[hreflang] = title
    return details


def parse_image_wikipedia(hreflang, wiki_html, details: ListItemDetails):
    image = wiki_html.select_one(
        "#mw-content-text > div > table.infobox > tbody > tr:nth-child(2) img"
    )
    # Картинка в карточке вида (при этом не карта распространения)
    if image is not None:
        if image.get("alt", None) == "edit":
            return details  # картинка карандаша
        src = "https:" + str(image['src'])
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


def copy_db_to_sqlite(where: str = None):
    """
    Скопируем базу Postgres в файл SQLite
    """
    print("Скопируем базу Postgres в файл SQLite")
    query = """
        SELECT id,
           title,
           page_url,
           type,
           image_url,
           wikipedias_by_languages,
           parent_page_url,
           parent_id,
           titles_by_languages
        FROM public.list
    """
    if where is not None and where != "":
        query += "WHERE " + where
    query += "\nORDER BY title;"
    list_iterator = DbListItemsIterator('copy_db_to_sqlite:list', query)

    item_counter = 0
    while True:
        list_item = list_iterator.fetchone()
        if not list_item:
            break

        print("Копирование в SQLite: {}".format(db_functions_sqlite.quote_nullable(list_item[1])))
        sql = """
            INSERT INTO list(id, title, page_url, type, image_url, wikipedias_by_languages, parent_page_url, parent_id, titles_by_languages)
            VALUES ({id}, {title}, {page_url}, {type}, {image_url}, {wikipedias_by_languages}, {parent_page_url}, {parent_id}, {titles_by_languages})
            /*ON CONFLICT(page_url) DO UPDATE
              SET title = excluded.title,
                page_url = excluded.page_url,
                type = excluded.type,
                image_url = excluded.image_url,
                wikipedias_by_languages = excluded.wikipedias_by_languages,
                parent_page_url = excluded.parent_page_url,
                parent_id = excluded.parent_id,
                titles_by_languages = excluded.titles_by_languages*/
            ;
        """.format(
            id=list_item[0],
            title=db_functions_sqlite.quote_nullable(list_item[1]),
            page_url=db_functions_sqlite.quote_nullable(list_item[2]),
            type=db_functions_sqlite.quote_nullable(list_item[3]),
            image_url=db_functions_sqlite.quote_nullable(list_item[4]),
            wikipedias_by_languages=db_functions_sqlite.quote_nullable(list_item[5]),
            parent_page_url=db_functions_sqlite.quote_nullable(list_item[6]),
            parent_id=db_functions_sqlite.nonquoted_nullable(list_item[7]),
            titles_by_languages=db_functions_sqlite.quote_nullable(list_item[8])
        )
        db_functions_sqlite.DbExecuteNonQuery.execute("copy_db_to_sqlite:insert", sql)

        item_counter += 1

    print("Копирование в SQLite закончено! Всего скопировано {} записей.".format(item_counter))




if __name__ == "__main__":
    main()
