from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from datetime import datetime, timedelta
import statistics
import copy
import math
from typing import TypedDict, Tuple, List, Dict
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
BASERATE = 2310 / 60  # mean per minute / 60
RUNTIME = 300

# in Python dictionaries are O(1), while lists are O(n)
# https://stackoverflow.com/questions/38927794/python-dictionary-vs-list-which-is-faster
# hence use dictionary of dictionaries
STARTING_ASSETS = {
        'buyCursor': {'price': 15, 'owned': 0, 'rate': 1},
        'buyGrandma': {'price': 100, 'owned': 0, 'rate': 0},
        'buyFactory': {'price': 500, 'owned': 0, 'rate': 20},
        'buyMine': {'price': 2000, 'owned': 0, 'rate': 50},
        'buyShipment': {'price': 7000, 'owned': 0, 'rate': 100},
    }


class DetailsDict(TypedDict):
    price: int
    owned: int
    rate: int


class AssetsDict(TypedDict):
    buyCursor: DetailsDict
    buyGrandma: DetailsDict
    buyFactory: DetailsDict
    BuyMine: DetailsDict
    buyShipment: DetailsDict


def main():
    assets = copy.deepcopy(STARTING_ASSETS)
    assets = update_grandma_rate(assets)

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=RUNTIME)
    print(start_time)
    print(end_time)

    assets = update_grandma_rate(assets)
    next_buy = find_best_roi_timehorizon(0, BASERATE, assets, RUNTIME)
    driver = open_page(DRIVER_EXE, URL)

    while end_time > datetime.now():
        click_cookie(driver)
        try:
            next_buy, assets = strategy3_best_roi_timehorizon(driver, next_buy, assets, end_time)
        except StaleElementReferenceException:
            continue

    cash = count_cookies(driver)
    assets = spend_leftovers(driver, assets, cash)

    # would expect 30 * 60 = 1800 clicks per minute
    # number of clicks per minute over 30 observations:

    observations = [
        2299, 2279, 2321, 2358, 2367, 2304, 2297, 2288, 2295, 2345,
        2301, 2232, 2314, 2288, 2345, 2365, 2347, 2366, 2366, 2366,
        2295, 2246, 2297, 2283, 2291, 2308, 2306, 2301, 2274, 2277,
    ]
    print(statistics.mean(observations))  # 2310
    print(statistics.median(observations))  # 2301
    # so, 11 505 - 11 550 clicks in 5 minutes


def click_cookie(driver: webdriver.Chrome) -> None:
    cookie = driver.find_element(By.ID, value='cookie')
    cookie.click()


def update_grandma_rate(assets: AssetsDict) -> AssetsDict:
    if assets['buyGrandma']['rate'] < 10:
        grandma_rate = 4
        if assets['buyFactory']['owned'] > 0:
            grandma_rate += 1
        if assets['buyMine']['owned'] > 0:
            grandma_rate += 2
        if assets['buyShipment']['owned'] > 0:
            grandma_rate += 3
        assets['buyGrandma']['rate'] = grandma_rate
    return assets


def strategy1_buy_available(driver: webdriver.Chrome, assets: AssetsDict) -> None:
    '''
    Function implements the naive approach of buying the highest yielding asset
    that we have enough cookies to acquire

    Over 5 minutes of runtime we end up with approx.
    31 - Cursors
    13 - GrandMas
    0 - Factories
    0 - Mines
    16.6 - cookie rate
    '''
    for div in reversed(list(assets.keys())):
        check_div = driver.find_element(By.ID, value=div)
        if check_div.get_attribute('class') != 'grayed':
            check_div.click()


def strategy2_best_roi(driver: webdriver.Chrome, next_buy: str, assets: AssetsDict) -> Tuple[str, AssetsDict]:
    '''
    Function implements a strategy of waiting to accrue enough cookies
    to acquire the asset with the highest ROI

    Over 5 minutes of runtime (+ spend_leftover) we end up with approx.
    13 + 4 - Cursors
    15 - GrandMas
    9 + 1 - Factories
    4 - Mines
    104.4 - cookie rate
    '''

    if check_if_available(driver, next_buy):
        assets = acquire(driver, next_buy, assets)
        assets = refresh_price(driver, next_buy, assets)
        assets = update_grandma_rate(assets)
        next_buy = find_best_roi(assets)
    return next_buy, assets


def strategy3_best_roi_timehorizon(
    driver: webdriver.Chrome, next_buy: str, assets: AssetsDict, end_time: datetime
) -> Tuple[str, AssetsDict]:
    '''
    Function implements a strategy of waiting to accrue enough cookies
    to acquire the asset with the highest ROI, if there is enough remaining time

    Over 5 minutes of runtime (+ spend_leftover) we end up with approx.
    13 + 3 - Cursors
    14 + 1 - GrandMas
    8 - Factories
    5 - Mines
    106.2 - cookie rate
    '''

    if check_if_available(driver, next_buy):
        assets = acquire(driver, next_buy, assets)
        assets = refresh_price(driver, next_buy, assets)
        assets = update_grandma_rate(assets)
        # this does not work because cookies don't drop instantaneously, it tends to get a false value
        cash = count_cookies(driver)
        rate = get_rate(driver) + BASERATE
        time_remaining = (end_time - datetime.now()).total_seconds()
        next_buy = find_best_roi_timehorizon(cash, rate, assets, time_remaining)
    return next_buy, assets


def find_best_roi(assets: AssetsDict) -> str:
    sorted_assets = find_best_roi_array(assets)
    best_asset = str(list(sorted_assets.keys())[0])
    return best_asset


def find_best_roi_array(assets: AssetsDict) ->Dict:
    best_roi ={}
    for asset in list(assets.keys()):
        best_roi[asset] = assets[asset]['rate'] / assets[asset]['price']
    sorted_best_roi = dict(sorted(best_roi.items(), key = lambda x:x[1], reverse = True))
    return sorted_best_roi  


def find_best_roi_timehorizon(cash:int, rate: float, assets: AssetsDict, time_remaining:int) ->str:
    sorted_best_roi = find_best_roi_array(assets)    
    cash_till_end = cash + rate * time_remaining
    for asset in sorted_best_roi.keys():
        if assets[asset]['price']< cash_till_end:
            return asset


def check_if_available(driver: webdriver.Chrome, asset: str) -> bool:
    try:
        check_div = driver.find_element(By.ID, value=asset)
        if check_div.get_attribute('class') != 'grayed':
            return True
    except StaleElementReferenceException:
        return False
    return False


def refresh_price(driver: webdriver.Chrome, asset: str, assets: AssetsDict) -> AssetsDict:
    got_price = False
    while not got_price:
        try:
            div = driver.find_element(By.CSS_SELECTOR, value=f'#{asset} b')
            price = int(div.text.split('- ')[1].replace(',', ''))
            assets[asset]['price'] = price
            got_price = True
        except StaleElementReferenceException:
            continue
    return assets


def acquire(driver: webdriver.Chrome, asset: str, assets: AssetsDict) -> AssetsDict:
    div = driver.find_element(By.ID, value=asset)
    div.click()
    assets[asset]['owned'] += 1
    return assets


def count_cookies(driver: webdriver.Chrome) -> int:
    div = driver.find_element(By.ID, value='money')
    money = int(div.text.replace(',',''))
    return money


def get_rate(driver: webdriver.Chrome) ->float:
    div = driver.find_element(By.ID, value='cps')
    rate = float(div.text.split(': ')[1])
    return rate


def spend_leftovers(driver: webdriver.Chrome, assets: AssetsDict, cash) -> AssetsDict:
    local_assets = copy.deepcopy(assets)

    while len(local_assets.items()) > 0:
        for asset in list(local_assets.keys()):
            if assets[asset]['price'] > cash:
                del local_assets[asset]

        if len(local_assets.items()) > 0:
            best_asset = find_best_roi(local_assets)
            try:
                assets = acquire(driver, best_asset, assets)

            except StaleElementReferenceException:
                continue
            else:
                price = assets[best_asset]['price']
                price_refreshed = False
                while not price_refreshed:
                    try:
                        assets = refresh_price(driver, best_asset, assets)
                        price_refreshed = True
                    except StaleElementReferenceException:
                        continue
                cash -=price

    return assets


if __name__ == '__main__':
    main()
