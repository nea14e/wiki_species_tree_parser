# -*- coding: utf-8 -*-
import traceback

import os
from selenium import webdriver
import time

from selenium.common.exceptions import WebDriverException

def get_levels(driver):
    # TODO по ссылкам где нет кнопки "показать" пропускает информацию(Скорей всего там другая структура HTML), сделать реплейс <b> и </b> в результате на пустоту
    parsed_levels = []
    infobox = driver.find_element_by_xpath('//table[@class="infobox"]')
    levels = infobox.find_elements_by_xpath('.//div[@class="NavFrame collapsed"]/div')
    for level in reversed(levels):
        if level != levels[0]: #Если 1 элемент(ненужный) то пропускаем
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
        else: pass
    return parsed_levels


class ParsedLevel:
    pass


def parse_list_for_kingdom(kingdom_list_url):
    links_mas = [] # Массив ссылок на странице
    driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(), 'geckodriver'))
    driver.get(kingdom_list_url)
    time.sleep(1)
    driver.implicitly_wait(2)
    item_counter = 0

    while True: # Цикл перехода на след. страницу
        try:
            next_page = driver.find_element_by_xpath('//div[@id="mw-pages"]/a[2]').get_attribute("href") # След. страница
        except:
            print('Все страницы списка обработаны')
            break
        for link in driver.find_elements_by_xpath('//div[@class="mw-category-group"]/ul/li/a'): #Цикл заполнения "массива ссылок на странице" ссылками, чтобы по ним переходить
            try:
                details_page_url = link.get_attribute("href") #Ссылка
                links_mas.append(details_page_url) #Добовляем ссылку в массив
            except:
                print('Ошибка:\n', traceback.format_exc())
        for link in links_mas: #Цикл по "массиву ссылок на странице"
            try:
                driver.get(link) #Переход по ссылке
                print('\n')
                print('===========================================')
                print('ССЫЛКА: ' + str(link))
                get_levels(driver) #Парсинг информации
                item_counter += 1
                time.sleep(1)
            except WebDriverException:
                print('Ошибка:\n', traceback.format_exc())
        driver.get(next_page) #Переходим на след страницу
        links_mas = [] #Чистим "массив ссылок на странице" для повтороной итерации
    print('ЦАРСТВО ' + kingdom_list_url + ' БЫЛО ОБРАБОТАНО!')
    driver.quit()

kingdom_animals_url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0' \
                      '%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1' \
                      '%82%D1%83'
kingdom_plants_url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D0' \
                     '%B0%D1%81%D1%82%D0%B5%D0%BD%D0%B8%D1%8F_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82' \
                     '%D1%83'
kingdom_mushrooms_url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93' \
                        '%D1%80%D0%B8%D0%B1%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
kingdom_viruses_url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%92%D0' \
                      '%B8%D1%80%D1%83%D1%81%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
# Выберите нужное и подставьте сюда перед запуском
parse_list_for_kingdom(kingdom_animals_url)
