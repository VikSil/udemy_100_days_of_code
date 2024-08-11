from selenium import webdriver

from typing import Tuple
from datetime import datetime

from custom_types import AssetsDict

from gui_utils import check_if_available, acquire, refresh_price, count_cookies, get_rate
from calc_utils import update_grandma_rate, find_best_roi_timehorizon


def strategy3_best_roi_timehorizon(
    driver: webdriver.Chrome, next_buy: str, assets: AssetsDict, end_time: datetime, base_rate: float
) -> Tuple[str, AssetsDict]:
    '''
    Function implements a strategy of waiting to accrue enough cookies
    to acquire the asset with the highest ROI, if there is enough remaining time

    Over 5 minutes of runtime we end up with approx.
    15 - Cursors
    14 - GrandMas
    7 - Factories
    3 - Mines
    80.6 - cookie rate
    '''

    if check_if_available(driver, next_buy):
        assets = acquire(driver, next_buy, assets)
        assets = refresh_price(driver, next_buy, assets)
        assets = update_grandma_rate(assets)
        # this does not work because cookies don't subtract the cost of purchase instantaneously
        # the cost of purchase is subtracted in chunks for some reason
        # hence, the driver tends to get a faulty value
        cash = count_cookies(driver)
        rate = get_rate(driver) + base_rate
        time_remaining = (end_time - datetime.now()).total_seconds()
        next_buy = find_best_roi_timehorizon(cash, rate, assets, time_remaining)
    return next_buy, assets
