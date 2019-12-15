# -*- coding: utf-8 -*-
import json
import platform
import re
import sys
import traceback

import os

import requests
from requests.utils import requote_uri
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options

from db_functions import DbFunctions, DbListItemsIterator, DbExecuteNonQuery, quote_nullable

IS_DEBUG = False
IS_HEADLESS = True  # Можно ещё для ускорения сделать через requests.

BROWSER_LOAD_TIMEOUT = 1
PAGE_LOAD_TIMEOUT = 1
NEXT_PAGE_DELAY = 3

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

    if platform.system() == 'Linux':
        geckodriver_name = 'geckodriver'
    else:
        geckodriver_name = 'geckodriver.exe'
    geckodriver_path = os.path.join(os.getcwd(), geckodriver_name)
    options = Options()
    if IS_HEADLESS:
        options.headless = True
    driver = webdriver.Firefox(executable_path=geckodriver_path, options=options)
    time.sleep(BROWSER_LOAD_TIMEOUT)

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
        populate_list(driver, from_title, to_title)  # 1 этап
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
        parse_details(driver, skip_parsed_interval, where)  # 2 этап
    elif stage_number == '3':
        if len(sys.argv) >= 3:
            where = sys.argv[2]
        else:
            where = ""
        correct_parents(where)  # 3 этап
    else:
        print_usage()

    driver.quit()


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


def populate_list(driver, from_title: str = "", to_title: str = ""):
    print("ЗАПУЩЕН 1 ЭТАП - СОСТАВЛЕНИЕ СПИСКА. Ограничения: с '{}' по '{}'".format(from_title, to_title))

    driver.get(
        "https://species.wikimedia.org/wiki/Special:AllPages?from={}&to={}&namespace=0" \
            .format(requote_uri(from_title), requote_uri(to_title))
    )
    time.sleep(PAGE_LOAD_TIMEOUT)

    succeeds = 0
    skipped = 0
    errors = 0
    while True:  # Цикл перехода на след. страницу
        # Cсылка на следующую страницу
        navigate_page_elems = driver.find_elements_by_xpath("//div[@class='mw-allpages-nav']/a")
        next_page_elem = None
        for el in navigate_page_elems:
            if "Next page" in el.text:
                next_page_elem = el
                break

        # Адрес из ссылки на следующую страницу
        if next_page_elem:
            next_page_url = next_page_elem.get_attribute("href")
        else:
            next_page_url = None

        # Сохраем в базу ссылки, чтобы потом по ним переходить
        for link in driver.find_elements_by_xpath("//ul[@class='mw-allpages-chunk']/li/a"):
            try:
                item_title = link.text
                if "." in item_title:  # Пропускаем имена учёных (с инициалами, поэтому у них точки)
                    skipped += 1
                    continue
                item_title = item_title.replace("'", "''")  # Экранирование для базы
                item_details_href = str(link.get_attribute("href"))
                item_details_href = item_details_href[len(URL_START):]  # Ссылка (без начала)
                # print("Новый элемент в списке для парсинга: '%s', '%s'" % (item_title, item_details_href))  # debug only
                DbFunctions.add_list_item(item_title, item_details_href)
                succeeds += 1
            except WebDriverException:
                errors += 1
                print('Ошибка:\n', traceback.format_exc())

        if next_page_url:
            print("Страница обработана. Следующая - {}. Всего успешно {} элементов, {} пропущено, {} ошибок.".format(
                next_page_elem.text, succeeds, skipped, errors))
            driver.get(next_page_url)  # Переходим на след страницу
            time.sleep(NEXT_PAGE_DELAY)
        else:
            print(
                "ВЕСЬ СПИСОК СОСТАВЛЕН! Всего успешно {} элементов, {} пропущено, {} ошибок.".format(succeeds, skipped,
                                                                                                     errors))
            return


def parse_details(driver, skip_parsed_interval, where=""):
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
            driver.get(URL_START + details.page_url)
            time.sleep(PAGE_LOAD_TIMEOUT)

            # Парсинг информации
            all_content = driver.find_element_by_xpath("//div[@class='mw-parser-output']")
            details = parse_image_wikispecies(all_content, details)
            is_parent_found, details = parse_levels(all_content, details)
            details = parse_wikipedias(all_content, details)

            # Запись всех подробностей в базу
            # (только если нашли родителя - без родителей в дереве элементы не нужны)
            if is_parent_found:
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
            else:
                without_parents += 1

        except WebDriverException:
            print('Ошибка:\n', traceback.format_exc())
            errors += 1
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
    try:
        image = main_content.find_element_by_xpath(
            ".//div[@class='thumb tright']//img")  # Просто любая картинка справа в основном содержимом
        src = image.get_attribute('src')
        print("Картинка в Викивидах: " + str(src))
        details.image_url = src
    except WebDriverException:  # Картинки может не быть - всё равно обрабатывать эту страницу дальше
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

    Или вот пример:
    <p>
        Familia: <a href="https://species.wikimedia.org/wiki/Heliconiaceae" title="Heliconiaceae">Heliconiaceae</a>
        <br>
        Genus:
        <i>
            <a class="mw-selflink selflink">Heliconia</a>
        </i>
        <br>
        ...
    """
    levels_p = tree_box.find_element_by_xpath("./p[1]")
    levels_p_text = str(
        levels_p.text)  # Напр., "Familia: Euconulidae\nSubfamilia: Microcystinae\nGenus: Philonesia\nSubgenus: Aa\n..."
    levels_tags = levels_p.find_elements_by_xpath("./*")

    # Найдём category, value для текущего уровня

    is_current_found = False
    current_level_ind = None
    current_level_a = None
    for ind, level in enumerate(levels_tags):
        # Найдём сначала сам текущий уровень - у него value написано особой ссылкой:
        current_level_a_s = level.find_elements_by_xpath("./a[@class='mw-selflink selflink']")
        if len(current_level_a_s) == 0:
            continue  # эта ссылка НЕ в просматриваемом нами уровне, пропускаем

        # эта ссылка ЕСТЬ в просматриваемом нами уровне
        current_level_ind = ind
        current_level_a = current_level_a_s[0]
        is_current_found = True
        break

    # Если текущий уровень почему-то не найден
    if not is_current_found:
        print("Ошибка: текущий уровень не найден!")
        return False, details

    details.title = current_level_a.text
    print("Текущий уровень - название: {}".format(details.title))

    # текст на текущем уровне до названия (напр., для уровня "Genus: Philonesia" это будет "Genus: ")
    text_before_title = levels_p_text[0: levels_p_text.index(current_level_a.text)].split('\n')[-1]
    # текст на текущем уровне до двоеточия
    details.type = text_before_title.split(':')[0]
    print("Текущий уровень - тип: {}".format(details.type))

    # Найдём category, value для предыдущего уровня

    ind = current_level_ind - 2  # предпредыдущий тег - пропускаем тег <br>
    if ind >= 0:
        prev_level_a = levels_tags[ind]
        prev_href = str(prev_level_a.get_attribute("href"))
        if prev_href == "None":
            prev_href = str(prev_level_a.find_element_by_xpath("./a").get_attribute("href"))
        details.parent_page_url = prev_href[len(URL_START):]
        if details.parent_page_url is None or details.parent_page_url == "None":
            details.parent_page_url = prev_href[len("/wiki/"):]
        print("Предыдущий уровень - ссылка: {}".format(details.parent_page_url))

        if IS_DEBUG:
            details.parent_title = prev_level_a.text
            print("Предыдущий уровень - название: {}".format(details.parent_title))

            # текст на предыдущем уровне до названия (напр., для уровня "Genus: Philonesia" это будет "Genus: ")
            text_before_title = levels_p_text[0: levels_p_text.index(prev_level_a.text)].split('\n')[-1]
            # текст на предыдущем уровне до двоеточия
            details.parent_type = text_before_title.split(':')[0]
            print("Предыдущий уровень - тип: {}".format(details.parent_type))

        return True, details
    else:
        print("Предыдущий уровень - не найден!")
        return False, details


def parse_wikipedias(driver, details: ListItemDetails):
    # Ссылки на Википедии разных языков
    try:
        a_s = driver.find_elements_by_xpath("//div[@id='p-lang']/div/ul/li/a")
        for a in a_s:
            if a.text != "":
                match = re.search(WIKIPEDIAS_URL_MASK, a.get_attribute("href"))
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
    except WebDriverException:
        print("Ошибка: Ссылки на Википедию НЕ НАЙДЕНЫ")
    return details


def parse_one_wikipedia(hreflang, wiki_html, details: ListItemDetails):
    title = wiki_html.select_one("div#content > h1").text
    if IS_DEBUG:
        print("Ссылка на Википедию: язык: {} заголовок: {}".format(hreflang, title))
    details.titles_by_languages[hreflang] = title
    return details


def parse_image_wikipedia(hreflang, wiki_html, details: ListItemDetails):
    image = wiki_html.select_one(
        "#mw-content-text > div > table.infobox > tbody > tr:nth-child(2) img"
    )
    # Картинка в карточке вида (при этом не карта распространения)
    if image is not None:
        src = "https:" + str(image['src'])
        print("Картинка в Википедии: язык: {} картинка: {}".format(hreflang, src))
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
