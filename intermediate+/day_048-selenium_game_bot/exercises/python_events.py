from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
from typing import Dict,TypedDict

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) # add parent dir to path to import upstream modules

from  utils import open_page

BASE_DIR = Path(__file__).resolve().parent.parent
URL = 'https://www.python.org/'
DRIVER_EXE = BASE_DIR / '../../chromedriver.exe'


class EventDict(TypedDict):
    time: str
    name: str


def main():
    driver = open_page(DRIVER_EXE, URL)
    events = get_events(driver)
    print(events)


def get_events(driver:webdriver.Chrome) -> Dict[int, EventDict]:

    times = driver.find_elements(By.CSS_SELECTOR, value = '.event-widget li time')
    names = driver.find_elements(By.CSS_SELECTOR, value = '.event-widget li a')
    event_list = [{'time': t.text, 'name': n.text} for t, n in zip(times, names)]  # make a list of dictionaries
    events = dict(enumerate(event_list)) # make enumerated dictionary of dictionaries

    return events


if __name__ == '__main__':
    main()
