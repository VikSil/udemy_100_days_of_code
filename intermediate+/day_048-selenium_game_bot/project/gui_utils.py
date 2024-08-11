from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

import copy
from typing import List
from datetime import datetime

from custom_types import AssetsDict
from calc_utils import find_best_roi


def acquire(driver: webdriver.Chrome, asset: str, assets: AssetsDict) -> AssetsDict:
    '''
    Function clicks on an asset and updates owned asset count
    '''
    div = driver.find_element(By.ID, value=asset)
    div.click()
    assets[asset]['owned'] += 1
    return assets


def acquire_no_accounting(driver: webdriver.Chrome, asset: str) -> None:
    '''
    Function clicks on an asset
    '''
    div = driver.find_element(By.ID, value=asset)
    div.click()


def check_if_available(driver: webdriver.Chrome, asset: str) -> bool:
    '''
    Function checks if it is possible to buy an asset (if it is enabled)
    '''
    try:
        check_div = driver.find_element(By.ID, value=asset)
        if check_div.get_attribute('class') != 'grayed':
            return True
    except StaleElementReferenceException:
        return False
    return False


def click_cookie(driver: webdriver.Chrome) -> None:
    '''
    Function sends mouse click to a cookie
    '''
    cookie = driver.find_element(By.ID, value='cookie')
    cookie.click()


def count_cookies(driver: webdriver.Chrome) -> int:
    '''
    Function scrapes the current number of accrued cookies
    '''
    div = driver.find_element(By.ID, value='money')
    money = int(div.text.replace(',', ''))
    return money


def get_rate(driver: webdriver.Chrome) -> float:
    '''
    Function scrapes the current accrual rate
    '''
    div = driver.find_element(By.ID, value='cps')
    rate = float(div.text.split(': ')[1])
    return rate


def refresh_price(driver: webdriver.Chrome, asset: str, assets: AssetsDict) -> AssetsDict:
    '''
    Function scrapes and updates the current price of an asset
    '''
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


def run_precalculated_strategy(driver: webdriver.Chrome, asset_chain: List) -> List:
    '''
    Function acquires assets in a precalculated order
    '''
    if len(asset_chain) > 0:
        next_buy = asset_chain[0]
        if check_if_available(driver, next_buy):
            acquire_no_accounting(driver, next_buy)
            asset_chain.pop(0)
    else:
        print(f'Chain too short at {datetime.now()}')
    return asset_chain


def spend_leftovers(driver: webdriver.Chrome, assets: AssetsDict, cash) -> AssetsDict:
    '''
    Function acquires assets with the cookie cash left over after the main strategy is run
    '''
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
                cash -= price

    return assets
