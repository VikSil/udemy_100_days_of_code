from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from datetime import datetime, timedelta
import statistics
from typing import TypedDict, Tuple
from selenium.common.exceptions import StaleElementReferenceException

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
BASERATE = 2310 / 12 # mean per minute / 5 second intervals per minute

class DetailsDict(TypedDict):
    price :int
    owned:int
    rate:int


class ArtifactsDict(TypedDict):
    buyCursor : DetailsDict
    buyGrandma : DetailsDict
    buyFactory : DetailsDict
    BuyMine : DetailsDict
    buyShipment : DetailsDict


def main():
    driver = open_page(DRIVER_EXE, URL)
    # in Python dictionaries are O(1), while lists are O(n)
    # https://stackoverflow.com/questions/38927794/python-dictionary-vs-list-which-is-faster
    # hence use dictionary of dictionaries
    artifacts = {
        'buyCursor': {'price': 15, 'owned': 0, 'rate': 1},
        'buyGrandma': {'price': 100, 'owned': 0, 'rate': 0},
        'buyFactory': {'price': 500, 'owned': 0, 'rate': 20},
        'buyMine': {'price': 2000, 'owned': 0, 'rate': 50},
        'buyShipment': {'price': 7000, 'owned': 0, 'rate': 100},
}

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes = 5)
    print(start_time)
    print(end_time)

    artifacts = update_grandma_rate(artifacts)
    next_buy = find_best_roi(artifacts)

    while end_time >  datetime.now():    
        click_cookie(driver)
        try:
            next_buy, artifacts = strategy2_wait_for_best_roi(driver, next_buy, artifacts)
        except StaleElementReferenceException:
            continue

    # would expect 30 * 60 = 1800 clicks per minute
    # number of clicks per minute over 30 observations:

    observations =[2299, 2279, 2321, 2358, 2367, 2304, 2297, 2288, 2295, 2345,
                   2301, 2232, 2314, 2288, 2345, 2365, 2347, 2366, 2366, 2366,
                   2295, 2246, 2297, 2283, 2291, 2308, 2306, 2301, 2274, 2277]
    print(statistics.mean(observations)) # 2310
    print(statistics.median(observations)) # 2301
    # so, 11 505 - 11 550 clicks in 5 minutes

    print(artifacts)

def click_cookie(driver:webdriver.Chrome) ->None:
    cookie = driver.find_element(By.ID, value ='cookie')
    cookie.click()    

def update_grandma_rate(artifacts: ArtifactsDict) ->ArtifactsDict:
    if artifacts['buyGrandma']['rate'] < 10:
        grandma_rate = 4
        if artifacts['buyFactory']['owned'] > 0:
            grandma_rate +=1
        if artifacts['buyMine']['owned'] > 0:
            grandma_rate +=2
        if artifacts['buyShipment']['owned'] > 0:
            grandma_rate += 3
        artifacts['buyGrandma']['rate'] = grandma_rate
    return artifacts


def strategy1_buy_available(driver: webdriver.Chrome, artifacts: ArtifactsDict) -> None:
    '''
    Function implements the naive approach of buying the highest yielding artifact
    that we have enough cookies to acquire

    Over 5 minutes of runtime we end up with approx.
    31 - Cursors
    13 - GrandMas
    0 - Factories
    0 - Mines
    16.6 - cookie rate
    '''
    for div in reversed(list(artifacts.keys())):
        check_div = driver.find_element(By.ID, value=div)
        if check_div.get_attribute('class') != 'grayed':
            check_div.click()


def strategy2_wait_for_best_roi(
    driver: webdriver.Chrome, next_buy: str, artifacts: ArtifactsDict
) -> Tuple[str, ArtifactsDict]:
    '''
    Function implements a strategy of waiting to accrue enough cookies 
    to acquire the artifact with the highest ROI

    Over 5 minutes of runtime we end up with approx.
    12 - Cursors
    15 - GrandMas
    9 - Factories
    3 - Mines
    89.4 - cookie rate
    '''

    if check_if_available(driver, next_buy):
        artifacts = acquire(driver, next_buy, artifacts)
        artifacts = refresh_price(driver, next_buy, artifacts)
        artifacts = update_grandma_rate(artifacts)
        next_buy = find_best_roi(artifacts)
    return next_buy, artifacts


def find_best_roi(artifacts: ArtifactsDict) ->str:
    best_roi = 0
    best_artifact = ''
    for artifact in list(artifacts.keys()):
        roi = artifacts[artifact]['rate']/artifacts[artifact]['price']
        if roi > best_roi:
            best_roi = roi
            best_artifact = artifact
    return best_artifact


def check_if_available(driver: webdriver.Chrome, artifact:str) -> bool:
    try:
        check_div = driver.find_element(By.ID, value=artifact)
        if check_div.get_attribute('class') != 'grayed':
            return True
    except StaleElementReferenceException:
        return False
    return False


def refresh_price(driver: webdriver.Chrome, artifact:str, artifacts: ArtifactsDict) ->ArtifactsDict:
    got_price = False
    while not got_price:
        try:
            div = driver.find_element(By.CSS_SELECTOR, value=f'#{artifact} b')
            price = int(div.text.split('- ')[1].replace(',',''))
            artifacts[artifact]['price'] = price
            got_price = True
        except StaleElementReferenceException:
            continue
    return artifacts


def acquire(driver: webdriver.Chrome, artifact:str, artifacts: ArtifactsDict) ->ArtifactsDict:
    div = driver.find_element(By.ID, value=artifact)
    div.click()
    artifacts[artifact]['owned'] +=1
    return artifacts


if __name__ == '__main__':
    main()
