from selenium import webdriver

from typing import Tuple

from custom_types import AssetsDict
from gui_utils import check_if_available, acquire, refresh_price
from calc_utils import update_grandma_rate, find_best_roi


def strategy2_best_roi(driver: webdriver.Chrome, next_buy: str, assets: AssetsDict) -> Tuple[str, AssetsDict]:
    '''
    Function implements a strategy of waiting to accrue enough cookies
    to acquire the asset with the highest ROI

    Over 5 minutes of runtime we end up with approx.
    16 - Cursors
    14 - GrandMas
    9 - Factories
    3 - Mines
    88.8 - cookie rate
    '''

    if check_if_available(driver, next_buy):
        assets = acquire(driver, next_buy, assets)
        assets = refresh_price(driver, next_buy, assets)
        assets = update_grandma_rate(assets)
        next_buy = find_best_roi(assets)
    return next_buy, assets
