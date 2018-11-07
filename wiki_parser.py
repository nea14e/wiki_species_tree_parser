# -*- coding: utf-8 -*-

from selenium import webdriver
import time

def get_levels(driver):
    infobox = driver.find_element_by_xpath('//table[@class="infobox"]')
    levels = infobox.find_elements_by_xpath('.//div[@class="NavFrame collapsed"]/div')
    for level in reversed(levels):
        category_html = level.find_element_by_xpath('.//td[1]')
        try:
            category = category_html.find_element_by_xpath('.//span').get_attribute('innerHTML')
        except:
            category = category_html.text
        # print(category)

        value_html = level.find_element_by_xpath('.//td[2]')
        try:
            value = value_html.find_element_by_xpath('.//a').get_attribute("innerHTML")
        except:
            try:
                value = value_html.find_element_by_xpath('.//span').get_attribute("innerHTML")
            except:
                value = value_html.text
        print(category + ' ' + value)


driver = webdriver.Firefox()

try:
    driver.get("https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83")
    time.sleep(1)
    driver.implicitly_wait(1)


    details_page_url = driver.find_elements_by_xpath('//div[@class="mw-category-group"]/ul/li/a')[2].get_attribute("href")
    driver.get(details_page_url)

    get_levels(driver)

    #print(parent.find_elements_by_xpath('.//td[2]/a').get_attribute('outerHTML'))
    #print (driver.find_elements_by_xpath('//div[@class="mw-category-group"]/ul/li/a')[0].text)
except:
    print('Error')

driver.quit()

#[0].get_attribute("href")