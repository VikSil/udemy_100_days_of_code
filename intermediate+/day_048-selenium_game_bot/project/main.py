# Global imports
from selenium.common.exceptions import StaleElementReferenceException

import os
import sys
import inspect

import copy
from datetime import datetime, timedelta


# Local imports
from monte_carlo_utils import *
from gui_utils import *
from calc_utils import *
from custom_types import *

# imports from subdirecotries
from strategies import *

# Imports from parent dir
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  # add parent dir to path to import upstream modules

from utils import *


# Imports from root dir
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DRIVER_EXE = BASE_DIR / '../../../chromedriver.exe'


# Global variables
URL = 'http://orteil.dashnet.org/experiments/cookie/'
BASERATE = 1600 / 60  # mean per minute / 60
RUNTIME = 120
STRATEGY = 4
PRECALCED = True

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

STRATEGIES = {
    1: 'strat1.strategy1_buy_available(driver, STARTING_ASSETS)',
    2: 'strat2.strategy2_best_roi(driver,find_best_roi(assets), assets)',
    3: 'strat3.strategy3_best_roi_timehorizon(driver,find_best_roi(assets),assets, end_time,BASERATE)',
}

PRECALC_STRATEGIES = {
    1: 'asset_chain = strat1_precalced.precalculate_strategy1(RUNTIME,BASERATE,assets)',
    2: 'asset_chain = strat2_precalced.precalculate_strategy2(RUNTIME,BASERATE,assets)',
    4: 'asset_chain = strat4_precalced.precalculate_strategy4(RUNTIME,BASERATE,assets)',
}


def main():
    assets = copy.deepcopy(STARTING_ASSETS)
    assets = update_grandma_rate(assets)

    if PRECALCED:
        asset_chain = None
        ldic = locals()
        try:
            exec(PRECALC_STRATEGIES[STRATEGY], globals(), ldic)
        except KeyError:
            sys.exit('Wrong strategy number')
        asset_chain = ldic['asset_chain']

        strategy_call = f'run_precalculated_strategy(driver, asset_chain)'
    else:
        try:
            strategy_call = STRATEGIES[STRATEGY]
        except KeyError:
            sys.exit('Wrong strategy number')

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=RUNTIME + 10)  # it takes about 10 seconds for the page to open

    driver = open_page(DRIVER_EXE, URL)
    print()
    print(f'Start at {start_time}')
    print(f'Expected end time at {end_time}')
    print()

    while end_time > datetime.now():
        click_cookie(driver)
        try:
            ldic = locals()
            exec(strategy_call, globals(), ldic)
            if PRECALCED:
                asset_chain = ldic['asset_chain']
        except StaleElementReferenceException:
            continue

    print('Remaining asset chain')
    print(asset_chain)
    cash = count_cookies(driver)
    assets = spend_leftovers(driver, assets, cash)


if __name__ == '__main__':
    main()
