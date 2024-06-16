from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from datetime import datetime, timedelta
import statistics

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  # add parent dir to path to import upstream modules

from utils import open_page

BASE_DIR = Path(__file__).resolve().parent
URL = 'http://orteil.dashnet.org/experiments/cookie/'
DRIVER_EXE = BASE_DIR / '../../../chromedriver.exe'

# in Python dictionaries are O(1), while lists are O(n)
# https://stackoverflow.com/questions/38927794/python-dictionary-vs-list-which-is-faster
# hence use dictionary of dictionaries
ARTIFACTS = {
    'cursor': {'price': 15, 'owned': 0, 'rate': 1},
    'grandma': {'price': 100, 'owned': 0, 'rate': 0},
    'factory': {'price': 500, 'owned': 0, 'rate': 20},
    'mine': {'price': 2000, 'owned': 0, 'rate': 50},
    'shipment': {'price': 7000, 'owned': 0, 'rate': 100},
    'lab': {'price': 50000, 'owned': 0, 'rate': 500},
}

BASERATE = 2310 / 12 # mean per minute / 5 second intervals per minute

def main():
    driver = open_page(DRIVER_EXE, URL)

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes = 1)
    print(start_time)
    print(end_time)

    while end_time >  datetime.now():    
        click_cookie(driver)
        update_grandma_rate()

    # would expect 30 * 60 = 1800 clicks per minute
    # number of clicks per minute over 30 observations:

    observations =[2299, 2279, 2321, 2358, 2367, 2304, 2297, 2288, 2295, 2345,
                   2301, 2232, 2314, 2288, 2345, 2365, 2347, 2366, 2366, 2366,
                   2295, 2246, 2297, 2283, 2291, 2308, 2306, 2301, 2274, 2277]
    print(statistics.mean(observations)) # 2310
    print(statistics.median(observations)) # 2301
    # so, 11 505 - 11 550 clicks in 5 minutes


def click_cookie(driver:webdriver.Chrome) ->None:
    cookie = driver.find_element(By.ID, value ='cookie')
    cookie.click()    

def update_grandma_rate():
    if ARTIFACTS['grandma']['rate']<14:
        grandma_rate = 4
        if ARTIFACTS['factory']['owned'] > 0:
            grandma_rate +=1
        if ARTIFACTS['mine']['owned'] > 0:
            grandma_rate +=2
        if ARTIFACTS['shipment']['owned'] > 0:
            grandma_rate += 3
        if ARTIFACTS['lab']['owned'] > 0:
            grandma_rate += 4
        ARTIFACTS['grandma']['rate'] = grandma_rate

if __name__ == '__main__':
    main()
