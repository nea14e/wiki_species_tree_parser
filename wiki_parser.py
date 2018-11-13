# -*- coding: utf-8 -*-
import traceback

import os
from selenium import webdriver
import time

from selenium.common.exceptions import WebDriverException

from db_functions import DbFunctions


def populate_list_for_kingdom(kingdom_title):
    kingdom_list_url = DbFunctions.get_kingdom_url(kingdom_title)

    driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(), 'geckodriver'))
    driver.get(kingdom_list_url)
    time.sleep(1)
    driver.implicitly_wait(5)
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
    print('ЦАРСТВО ' + kingdom_list_url + ' БЫЛО ОБРАБОТАНО! Всего успешно ' + str(item_counter) + " элементов добавлено в список.")
    driver.quit()


def parse_details(kingdom_title):
    kingdom_list_url = DbFunctions.get_kingdom_url(kingdom_title)
    # for link in links_mas:  # Цикл по "массиву ссылок на странице"
    # try:
    #     driver.get(link)  # TODO Переход по ссылке
    #     print('\n')
    #     print('===========================================')
    #     print('ССЫЛКА: ' + str(link))
    #     get_levels(driver)  # TODO Парсинг информации
    #     item_counter += 1
    #     time.sleep(1)
    # except WebDriverException:
    #     print('Ошибка:\n', traceback.format_exc())


def get_levels(driver):
    # TODO по ссылкам где нет кнопки "показать" пропускает информацию(Скорей всего там другая структура HTML),
    # TODO сделать реплейс <b> и </b> в результате на пустоту
    parsed_levels = []
    infobox = driver.find_element_by_xpath('//table[@class="infobox"]')
    levels = infobox.find_elements_by_xpath('.//div[@class="NavFrame collapsed"]/div')
    for level in reversed(levels):
        if level != levels[0]:  # Если 1 элемент(ненужный) то пропускаем
            parsed_level = ParsedLevel()
            category_html = level.find_element_by_xpath('.//td[1]')
            try:
                parsed_level.category = category_html.find_element_by_xpath('.//span').get_attribute('innerHTML')
            except WebDriverException:
                parsed_level.category = category_html.text
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
        else:
            pass
    return parsed_levels


class ParsedLevel:
    pass


# Выберите нужное и подставьте сюда перед запуском
DbFunctions.init_db()
populate_list_for_kingdom('mushrooms')
