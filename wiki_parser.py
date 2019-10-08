# -*- coding: utf-8 -*-
import platform
import sys
import traceback

import os

from requests.utils import requote_uri
from selenium import webdriver
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options

from db_functions import DbFunctions, DbListItemsIterator, DbExecuteNonQuery, quote_nullable

IS_HEADLESS = False

BROWSER_LOAD_TIMEOUT = 1
PAGE_LOAD_TIMEOUT = 1
NEXT_PAGE_DELAY = 3

# ! Внимание! Чтобы использовать Selenium, нужен Firefox версии не выше 66.
# Скачать его можно отсюда: https://ftp.mozilla.org/pub/firefox/releases/66.0.5/

URL_START = "https://species.wikimedia.org/wiki/"


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
                not_parsed_only = True
            elif sys.argv[2] == "False":
                not_parsed_only = False
            else:
                raise ValueError("Не удаётся прочитать bool: " + str(sys.argv[2]))
        else:
            not_parsed_only = True
        if len(sys.argv) >= 4:
            where = sys.argv[3]
        else:
            where = ""
        parse_details(driver, not_parsed_only, where)  # 2 этап

    driver.quit()


def print_usage():
    print("ОШИБКА: неизвестные параметры.")
    print("Запускайте через параметры командной строки")
    print("Для 0 этапа - инициализации базы:")
    print("0")
    print("Для 1 этапа - составления списка:")
    print("1 имя_царства")
    print("Для 2 этапа - получения деталей по списку:")
    print("2 имя_царства [bool(True только ещё не распарсенные, False для перезаписи)=True] [where_фильтр_на_список=\"\"]")


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
            print("Страница обработана. Следующая - {}. Всего успешно {} элементов, {} пропущено, {} ошибок.".format(next_page_elem.text, succeeds, skipped, errors))
            driver.get(next_page_url)  # Переходим на след страницу
            time.sleep(NEXT_PAGE_DELAY)
        else:
            print("ВЕСЬ СПИСОК СОСТАВЛЕН! Всего успешно {} элементов, {} пропущено, {} ошибок.".format(succeeds, skipped, errors))
            return


def parse_details(driver, kingdom_title, not_parsed_only, where=""):  # TODO parse_details() rework
    query = """
      SELECT id, title, page_url
      FROM public.list
      WHERE 1 = 1
      """
    if not_parsed_only:
        query += "AND type IS NULL "
    if where is not None and where != "":
        query += "AND " + str(where) + " "
    query += "ORDER BY title;"
    print("Список для парсинга:\n" + query)
    list_iterator = DbListItemsIterator("parse_details:list_to_parse", query)

    # Цикл по элементам из списка, подготовленного с помощью populate_list_for_kingdom()
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
            driver.get(details.page_url)
            time.sleep(PAGE_LOAD_TIMEOUT)

            # Парсинг информации
            all_content = driver.find_element_by_xpath("//div[@class='mw-parser-output']")
            details = parse_image(all_content, details)
            is_parent_found, details = parse_levels(all_content, details)

            # Запись всех подробностей в базу
            # (только если нашли родителя - без родителей в дереве элементы не нужны)
            if is_parent_found:
                query = """
                  UPDATE public.list
                  SET title = '{}'
                    , type = '{}'
                    , image_url = {}
                    , parent_type = {}
                    , parent_title = {}
                  WHERE id = '{}';
                """.format(
                    str(details.title)
                    , str(details.type)
                    , quote_nullable(details.image_url)
                    , quote_nullable(details.parent_type)
                    , quote_nullable(details.parent_title)
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
    print("ПАРСИНГ ЦАРСТВА " + str(kingdom_title) + " ОКОНЧЕН!")
    print("Добавлены детали о " + str(item_counter) + " элементов.")
    print("Не найдены родители для " + str(without_parents) + " элементов.")
    print("Ошибки для " + str(errors) + " элементов.")
    correct_parents()


class ListItemDetails:
    def __init__(self, id, title, page_url):
        self.id = id
        self.title = title
        self.page_url = page_url
        self.type = None
        self.image_url = None
        self.parent_type = None
        self.parent_title = None


def parse_image(main_content, details):
    try:
        image = main_content.find_element_by_xpath(".//div[@class='tright']//img")  # Просто любая картинка справа в основном содержимом
        src = image.get_attribute('src')
        print("Картинка: " + str(src))
        details.image_url = src
    except WebDriverException:  # Картинки может не быть - всё равно обрабатывать эту страницу дальше
        print("Картинка НЕ НАЙДЕНА")
        details.image_url = None
    return details


def parse_levels(tree_box, details):  # TODO test
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
    levels = levels_p.find_elements_by_xpath("./*")

    # Найдём category, value для текущего уровня

    is_current_found = False
    current_level_a = None
    for ind, level in enumerate(levels):
        # Найдём сначала сам текущий уровень - у него value написано особой ссылкой:
        current_level_a_s = level.find_elements_by_xpath("./a[@class='mw-selflink']")
        if len(current_level_a_s) == 0:
            continue  # эта ссылка НЕ в просматриваемом нами уровне, пропускаем

        # эта ссылка ЕСТЬ в просматриваемом нами уровне
        current_level_a = current_level_a_s[0]
        is_current_found = True
        break

    # Если иекущий уровень почему-то не найден
    if not is_current_found:
        print("Ошибка: текущий уровень не найден!")
        return False, details

    details.title = current_level_a.text
    print("Текущий уровень - название: {}".format(details.title))

    current_level_i = current_level_a.parent
    ind = levels.index(current_level_i) - 1  # предыдущий тег
    if ind >= 0:
        details.type = str(levels[ind].text).split(':')[0]  # текст до двоеточия
        print("Текущий уровень - тип: {}".format(details.type))
    else:
        print("Текущий уровень - тип - не найден!")

    # Найдём category, value для предыдущего уровня

    ind = ind - 2  # предпредыдущий тег - пропускаем тег <br>
    if ind >= 0:
        prev_level_a_s = levels[ind].find_elements_by_xpath("./a")
        if len(prev_level_a_s) > 0:
            prev_level_a = prev_level_a_s[0]
            details.parent_title = prev_level_a.text
            print("Предыдущий уровень - название: {}".format(details.parent_title))
        else:
            print("Предыдущий уровень - название - ссылка не найдена!")
    else:
        print("Предыдущий уровень - название - не найдено!")

    ind = ind - 1  # предыдущий тег
    if ind >= 0:
        details.parent_type = str(levels[ind].text).split(':')[0]  # текст до двоеточия
        print("Предыдущий уровень - тип: {}".format(details.parent_type))
    else:
        print("Предыдущий уровень - тип - не найден!")

    return True, details


def correct_parents(where: str = None):  # TODO rework
    """
    После парсинга списка пройдёмся по базе и заполним parent_id по parent_title.
    При None обрабатывает все царства.
    """
    print("Поправляем ссылки на родителей (построение дерева)...")
    query = "SELECT id, kingdom_id, parent_type, parent_title " \
            "FROM public.list " \
            "WHERE "
    if where is not None:
        query += where + \
                 "AND "
    query += " parent_title IS NOT NULL AND parent_id IS NULL;"  # Только у которых уже заполнен текст родителя, но ещё не привязаны
    list_iterator = DbListItemsIterator('parse_details:list_to_parse', query)

    # Цикл по элементам из списка, подготовленного с помощью populate_list_for_kingdom()
    item_counter = 0
    without_parents = 0
    while True:
        list_item = list_iterator.fetchone()
        if not list_item:
            break
        # Ищем родителя в базе по parent_title.
        # Проверим, есть ли такой элемент среди public.list,
        # используя level.value и kingdom_id - они уникальны в таблице list
        # (одно level.value может повторяться - есть растение и животное с одинаковым именем;
        # тип и имя использовать нельзя, т.к. тип level.category у родителя заполняется при парсинге родителя,
        # а он может быть ещё не распарсен).
        # Чтобы вершина дерева царства подцепилась к самому элементу Царство, надо, чтобы он в корне дерева имел
        # такой же kingdom_id, как само царство (потому что здесь при поиске родителя в WHERE подставляется
        # kingdom_id текущего элемента, а не самого родителя, т.е. считается, что они совпадают)
        #  - это примечание важно для заполнения файла db_init/list.csv.
        query = "SELECT id " \
                "FROM public.list " \
                "WHERE kingdom_id = " + str(list_item[1]) + \
                "  AND (type = " + quote_nullable(list_item[2]) + " OR type = '?' OR " + quote_nullable(list_item[2]) + " IS NULL) " \
                "  AND title = " + quote_nullable(list_item[3]) + \
                                                        "LIMIT 1;"
        parent_in_db_iter = DbListItemsIterator('parse_details:get_parent', query)
        if parent_in_db_iter.rowcount() > 0:
            # Нашли в базе данных запись о родителе
            parent_in_db = parent_in_db_iter.fetchone()[0]
            query = "UPDATE public.list " \
                    "SET parent_id = " + str(parent_in_db) + \
                    "WHERE id = " + str(list_item[0]) + ";"
            DbExecuteNonQuery.execute('parse_details:set_parent_id', query)
            item_counter += 1
        else:
            without_parents += 1
    print("\n")
    if kingdom_title is not None:
        print("ОБНОВЛЕНИЕ РОДИТЕЛЕЙ В ЦАРСТВЕ " + str(kingdom_title) + " ОКОНЧЕНО!")
    else:
        print("ОБНОВЛЕНИЕ РОДИТЕЛЕЙ ВО ВСЕХ ЦАРСТВАХ ОКОНЧЕНО!")
    print("Добавлены родители к " + str(item_counter) + " элементам.")
    print("Не найдены родители для " + str(without_parents) + " элементов.")


if __name__ == "__main__":
    main()
