from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path


import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  # add parent dir to path to import upstream modules

from utils import open_page

BASE_DIR = Path(__file__).resolve().parent
URL = 'https://en.wikipedia.org/wiki/Main_Page'
DRIVER_EXE = BASE_DIR / '../../../chromedriver.exe'


def main():
    driver = open_page(DRIVER_EXE, URL)
    count = get_article_count(driver)
    print(count)
    search_wiki(driver, "Python")


def get_article_count(driver: webdriver.Chrome) -> str:
    count = driver.find_element(By.CSS_SELECTOR, value='#articlecount a').text
    return count


def search_wiki(driver: webdriver.Chrome, keyword:str) -> None:
    search  = driver.find_element(By.NAME, value = "search")
    search.send_keys(keyword, Keys.ENTER)

if __name__ == '__main__':
    main()
