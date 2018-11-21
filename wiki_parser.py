# -*- coding: utf-8 -*-
import traceback

import os
from selenium import webdriver
import time

from selenium.common.exceptions import WebDriverException

from db_functions import DbFunctions, DbListItemsIterator, DbExecuteNonQuery, quote_nullable


def populate_list_for_kingdom(driver, kingdom_title):
    kingdom_list_url = DbFunctions.get_kingdom_url(kingdom_title)
    driver.get(kingdom_list_url)

    item_counter = 0

    while True:  # Цикл перехода на след. страницу
        # Cсылка на следующую страницу
        try:
            next_page_elem = driver.find_element_by_xpath('//div[@id="mw-pages"]/a[2]')
        except WebDriverException:
            next_page_elem = None
            pass

        # Адрес из ссылки на следующую страницу
        if next_page_elem:
            if next_page_elem.text == 'Следующая страница':
                next_page_url = next_page_elem.get_attribute("href")  # След. страница
            elif next_page_elem.text == 'Предыдущая страница':
                next_page_url = None
            else:
                raise Exception("Ссылка на следующую страницу не найдена")
        else:
            next_page_url = None

        # Сохраем в базу ссылки, чтобы потом по ним переходить
        for link in driver.find_elements_by_xpath(
                '//div[@class="mw-category-group"]/ul/li/a'):
            try:
                item_title = link.text  # Ссылка
                item_details_href = link.get_attribute("href")  # Ссылка
                print(
                    'Новый элемент в списке для парсинга: %s, %s, %s' % (kingdom_title, item_title, item_details_href))
                DbFunctions.add_list_item(kingdom_title, item_title, item_details_href)
                item_counter += 1
            except WebDriverException:
                print('Ошибка:\n', traceback.format_exc())

        if next_page_url:
            driver.get(next_page_url)  # Переходим на след страницу
            time.sleep(1)
        else:
            print('Все страницы списка обработаны')
            break
    print('ЦАРСТВО ' + kingdom_list_url + ' БЫЛО ОБРАБОТАНО! Всего успешно ' + str(
        item_counter) + " элементов добавлено в список.")


def parse_details(driver, kingdom_title):
    kingdom_id = DbFunctions.get_kingdom_id(kingdom_title)
    query = "SELECT id, title, page_url " \
            "FROM public.list " \
            "WHERE kingdom_id = '" + str(kingdom_id) + "';"
    list_iterator = DbListItemsIterator('parse_details:list_to_parse', query)

    # Цикл по элементам из списка, подготовленного с помощью populate_list_for_kingdom()
    item_counter = 0
    without_parents = 0
    errors = 0
    while True:
        list_item = list_iterator.fetchone()
        if not list_item:
            break
        try:
            details = ListItemDetails(list_item[0], kingdom_id, list_item[1], list_item[2])
            print('===========================================')
            print('ПОЛУЧАЕМ ДЕТАЛИ О: ' + details.title + " ссылка: " + details.page_url)
            driver.get(details.page_url)

            # Парсинг информации
            infobox = driver.find_element_by_xpath('//table[@class="infobox"]')
            details = parse_image(infobox, details)
            is_parent_found, details = parse_levels(infobox, details)

            # Запись всех подробностей в базу
            # (только если нашли родителя - без родителей в дереве элементы не нужны)
            if is_parent_found:
                query = "UPDATE public.list " \
                        "SET type = '" + str(details.type) + "' " \
                                                             "  , image_url = " + quote_nullable(details.image_url) + \
                        "  , parent_id = " + quote_nullable(details.parent_id) + \
                        "WHERE id = " + str(details.id) + ";"
                DbExecuteNonQuery.execute('parse_details:update_details', query)
                item_counter += 1
            else:
                without_parents += 1

            time.sleep(1)
        except WebDriverException:
            print('Ошибка:\n', traceback.format_exc())
            errors += 1
    print("ВЕСЬ СПИСОК ПО ЦАРСТВУ " + str(kingdom_title) + " ПРОЙДЕН!")
    print("Добавлены детали о " + str(item_counter) + " элементов.")
    print("Не найдены родители для " + str(without_parents) + " элементов.")
    print("Ошибки для " + str(errors) + " элементов.")


class ListItemDetails:
    def __init__(self, id, kingdom_id, title, page_url):
        self.id = id
        self.kingdom_id = kingdom_id
        self.title = title
        self.page_url = page_url
        self.type = None
        self.image_url = None
        self.parent_id = None


def parse_image(infobox, details):
    try:
        image = infobox.find_element_by_xpath('(./tbody/tr)[2]//img')
        src = image.get_attribute('src')
        print("Картинка: " + str(src))
        details.image_url = src
    except WebDriverException:  # Картинки может не быть - всё равно обрабатывать эту страницу дальше
        print("Картинка НЕ НАЙДЕНА" + traceback.format_exc())
        details.image_url = None
    return details


def parse_levels(infobox, details):
    """
            Парсим таблицу элементов-родителей, в которые вложен данный элемент
            (для черепах это будет что-то вроде
              Царство: Животные, Тип: Хордовые, Подтип: Позвоночные, Класс: Пресмыкающиеся, Отряд: Черепахи)
            Вытаскивает: тип текущего элемента (Отряд),
              название и тип ближайшего имеющегося в базе родителя (Класс: Пресмыкающиеся)
            """
    # TODO сделать реплейс <b> и </b> в результате на пустоту
    levels = infobox.find_elements_by_xpath('.//div[@class="NavFrame collapsed"]/div')
    if len(levels) == 0:
        levels = infobox.find_elements_by_xpath('(./tbody/tr/td/table)[1]/tbody/tr')
    is_parent_found = False
    for ind, level in enumerate(reversed(levels)):
        # Пропускаем самый верхний элемент иерархии
        # Прямым родителем он вряд ли когда будет, зато его парсить надо по-другому из-за "Показать промежуточные ранги"
        if ind == len(levels) - 1:
            continue
        parsed_level = ParsedLevel()
        category_html = level.find_element_by_xpath('.//td[1]')
        try:
            parsed_level.category = category_html.find_element_by_xpath('.//span').get_attribute('innerHTML')
        except WebDriverException:
            parsed_level.category = category_html.text
        parsed_level.category = str(parsed_level.category).rstrip(" ").rstrip(":")

        value_html = level.find_element_by_xpath('.//td[2]')
        try:
            parsed_level.value = value_html.find_element_by_xpath('.//a').get_attribute("innerHTML")
        except WebDriverException:
            try:
                parsed_level.value = value_html.find_element_by_xpath('.//span').get_attribute("innerHTML")
            except WebDriverException:
                parsed_level.value = value_html.text
        print(parsed_level.category + ' ' + parsed_level.value)

        # Самый нижний элемент - это сам тот, кого парсим. Там написан тип (это Вид, Род, Семейство или что ещё)
        if ind == 0:
            details.type = parsed_level.category
            print("Сам этот элемент: " + parsed_level.category + " " + parsed_level.value + " " + details.title)
        else:  # Все последующие за ним - кандидаты быть его прямым родителем
            # Родителя надо вычислить, чтобы к нему прикрепить текущий элемент - получится дерево.

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
                    "WHERE kingdom_id = " + str(details.kingdom_id) + \
                    "  AND title = '" + str(level.value) + "' " \
                                                           "LIMIT 1;"
            parent_in_db_iter = DbListItemsIterator('parse_details:get_parent', query)
            if parent_in_db_iter.rowcount() > 0:
                # Нашли в базе данных запись о родителе
                details.parent_id = parent_in_db_iter.fetchone()[0]
                is_parent_found = True
                print("Найден родитель: " + str(level.category) + " " + str(level.value))
                break  # Не считываем дальнейшую иерархию - это долго и не нужно
    return is_parent_found, details


class ParsedLevel:
    def __init__(self):
        self.category = ""
        self.value = ""


driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(), 'geckodriver'))
time.sleep(1)
driver.implicitly_wait(5)

DbFunctions.init_db()

# Выберите нужное и подставьте сюда перед запуском
# populate_list_for_kingdom(driver, 'mushrooms')
parse_details(driver, 'mushrooms')

driver.quit()
