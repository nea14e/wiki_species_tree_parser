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
            details = ListItemDetails(list_item[0], list_item[1], list_item[2])
            print('===========================================')
            print('ПОЛУЧАЕМ ДЕТАЛИ О: ' + details.title + " ссылка: " + details.page_url)
            driver.get(details.page_url)

            # Парсинг информации
            infobox = driver.find_element_by_xpath('//table[@class="infobox"]')

            # TODO парсить url картинки (её может не быть, не падать тогда в except, а всё равно добавлять)
            details.image_url = parse_image(infobox)

            # Парсим таблицу элементов-родителей, в которые вложен данный элемент
            # (для черепах это будет что-то вроде Животные, Хордовые, Позвоночные, Пресмыкающиеся)
            levels = get_levels(infobox)
            current_level = levels[0]
            details.type = current_level.category
            # Ищем родителя, к которому прикрепить этот элемент
            levels.pop(0)  # Сам текущий элемент (первый в списке) не может быть родителем
            is_parent_found = False
            for level in levels:
                # Проверим, есть ли такой элемент среди public.list, используя level.value и kingdom_id - они уникальны в таблице list:
                query = "SELECT id " \
                        "FROM public.list " \
                        "WHERE kingdom_id = " + str(kingdom_id) + \
                        "  AND title = '" + str(level.value) + "' " \
                                                               "LIMIT 1;"
                parent_in_db_iter = DbListItemsIterator('parse_details:get_parent', query)
                if parent_in_db_iter.rowcount() > 0:
                    # Нашли в базе данных запись о родителе
                    details.parent_id = parent_in_db_iter.fetchone()[0]
                    print("Найден родитель: " + str(level.category) + " " + str(level.value))

                    # Запись всех подробностей в базу
                    # (именно в этом месте кода, только если нашли родителя - без родителей в дереве элементы не нужны)
                    query = "UPDATE public.list " \
                            "SET type = '" + str(details.type) + "' " \
                            "  , image_url = " + quote_nullable(details.image_url) + \
                            "  , parent_id = " + quote_nullable(details.parent_id) + \
                            "WHERE id = " + str(details.id) + ";"
                    DbExecuteNonQuery.execute('parse_details:update_details', query)
                    is_parent_found = True
                    break

            if is_parent_found:
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
    def __init__(self, id, title, page_url):
        self.id = id
        self.title = title
        self.page_url = page_url
        self.type = None
        self.image_url = None
        self.parent_id = None


def get_levels(infobox):
    # TODO сделать реплейс <b> и </b> в результате на пустоту
    parsed_levels = []
    levels = infobox.find_elements_by_xpath('.//div[@class="NavFrame collapsed"]/div')
    if len(levels) == 0:
        levels = infobox.find_elements_by_xpath('(./tbody/tr/td/table)[1]/tbody/tr')
    for ind, level in enumerate(reversed(levels)):
        if ind == 0 or ind == len(levels) - 1:  # Если 1 элемент(ненужный) или последний(неправильный), то пропускаем
            continue
        parsed_level = ParsedLevel()
        category_html = level.find_element_by_xpath('.//td[1]')
        try:
            parsed_level.category = category_html.find_element_by_xpath('.//span').get_attribute('innerHTML')
        except WebDriverException:
            parsed_level.category = category_html.text
        parsed_level.category = str(parsed_level.category).rstrip(" ").rstrip(":")
        # print(category)

        value_html = level.find_element_by_xpath('.//td[2]')
        try:
            parsed_level.value = value_html.find_element_by_xpath('.//a').get_attribute("innerHTML")
        except WebDriverException:
            try:
                parsed_level.value = value_html.find_element_by_xpath('.//span').get_attribute("innerHTML")
            except WebDriverException:
                parsed_level.value = value_html.text
        print(parsed_level.category + ' ' + parsed_level.value)
        parsed_levels.append(parsed_level)
    return parsed_levels


def parse_image(infobox):
    try:
        image = infobox.find_element_by_xpath('(./tbody/tr)[2]//img')
        src = image.get_attribute('src')
        print("Картинка: " + str(src))
        return src
    except WebDriverException:
        print("Картинка НЕ НАЙДЕНА" + traceback.format_exc())
        return None



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
