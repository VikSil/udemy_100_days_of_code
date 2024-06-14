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
URL = 'https://secure-retreat-92358.herokuapp.com'
DRIVER_EXE = BASE_DIR / '../../../chromedriver.exe'


def main():
    driver = open_page(DRIVER_EXE, URL)
    fill_field(driver, 'fName', 'Jane')
    fill_field(driver, 'lName', 'Doe')
    fill_field(driver, 'email', 'jane.doe@domain.com')
    click_button(driver)


def fill_field(driver: webdriver.Chrome, name: str, text: str) -> None:
    field = driver.find_element(By.NAME, value=name)
    field.send_keys(text)


def click_button(driver: webdriver.Chrome) -> None:
    btn = driver.find_element(By.CLASS_NAME, value='btn-primary')
    btn.click()


if __name__ == '__main__':
    main()
