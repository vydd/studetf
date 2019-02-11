#!/usr/bin/env python3

import random
import time
import config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup


WAIT_TIME = 4


def login(driver, username, password):
    driver.get('https://student.etf.bg.ac.rs')
    username_field = driver.find_element_by_id('j_username')
    username_field.send_keys(username)
    password_field = driver.find_element_by_id('j_password')
    password_field.send_keys(password)
    driver.find_element_by_id('login').click()


def goto_surveys(driver):
    element = driver.find_element_by_id('menu_nav1_txt17')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(WAIT_TIME)


def find_surveys(driver):
    return driver.find_elements_by_class_name('okCancelButton')


def fill_in_survey(driver):
    driver.find_elements_by_css_selector('select > option')[-1].click()
    for x in driver.find_elements_by_css_selector('input[type="radio"]'):
        x.click()
    driver.find_element_by_id('main:finish')
    te = driver.find_elements_by_css_selector('textarea')[0]
    te.send_keys(str(random.randint(0, 10)))
    driver.find_element_by_id('main:finish').click()
    time.sleep(WAIT_TIME)
    driver.find_element_by_id('main:save').click()
    time.sleep(WAIT_TIME)


def go():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(
        options=options,
        executable_path=config.GECKODRIVER_PATH)
    login(driver, config.STUDENT_USERNAME, config.STUDENT_PASSWORD)
    goto_surveys(driver)
    surveys = find_surveys(driver)
    while surveys:
        surveys[0].click()
        time.sleep(WAIT_TIME)
        fill_in_survey(driver)
        surveys = find_surveys(driver)
    driver.close()
    return driver

if __name__ == '__main__':
    go()
