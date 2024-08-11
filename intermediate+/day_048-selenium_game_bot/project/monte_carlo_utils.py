from datetime import datetime, timedelta
import statistics

from gui_utils import click_cookie, count_cookies


import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  # add parent dir to path to import upstream modules
from utils import open_page


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DRIVER_EXE = BASE_DIR / '../../../chromedriver.exe'

URL = 'http://orteil.dashnet.org/experiments/cookie/'


def monte_carlo_clicker(batch_time: int, batch_count: int):

    sim_results = []

    for _ in range(batch_count):

        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=batch_time)

        driver = open_page(DRIVER_EXE, URL)
        while end_time > datetime.now():
            click_cookie(driver)

        sim_results.append(count_cookies(driver))
        driver.close()

    mean = statistics.mean(sim_results)
    median = statistics.median(sim_results)

    return mean, median
