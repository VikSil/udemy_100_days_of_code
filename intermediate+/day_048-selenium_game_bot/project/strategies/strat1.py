from selenium import webdriver
from selenium.webdriver.common.by import By

from custom_types import AssetsDict


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
