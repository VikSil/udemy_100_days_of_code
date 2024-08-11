import math
from typing import Dict

from custom_types import AssetsDict


def find_best_roi(assets: AssetsDict) -> str:
    '''
    Function returns the first ROI from a pre-sorted array of ROI
    '''
    sorted_assets = find_best_roi_array(assets)
    best_asset = str(list(sorted_assets.keys())[0])
    return best_asset


def find_best_roi_array(assets: AssetsDict) -> Dict:
    '''
    Function calculates ROI for a list of assets and sorts the list descending
    '''
    best_roi = {}
    for asset in list(assets.keys()):
        best_roi[asset] = assets[asset]['rate'] / assets[asset]['price']
    sorted_best_roi = dict(sorted(best_roi.items(), key=lambda x: x[1], reverse=True))
    return sorted_best_roi


def find_best_roi_timehorizon(cash: int, rate: float, assets: AssetsDict, time_remaining: int) -> str:
    '''
    Function returns the first ROI from a pre-sorted array of ROI
    that can be achieved in the remaining time
    '''
    sorted_best_roi = find_best_roi_array(assets)
    cash_till_end = cash + rate * time_remaining
    for asset in sorted_best_roi.keys():
        if assets[asset]['price'] < cash_till_end:
            return asset


def find_time_till_acquisition(assets: AssetsDict, rate: float) -> Dict:
    '''
    Function finds time till acquisition for all assets at a given accrual rate
    '''
    time_till_acquisition = {}
    for asset in list(assets.keys()):
        time_till_acquisition[asset] = math.ceil(assets[asset]['price'] / rate)
    return time_till_acquisition


def refresh_theo_price(asset: str, assets: AssetsDict) -> AssetsDict:
    '''
    Function increases price of a newly acquired asset
    '''
    curr_price = assets[asset]['price']
    assets[asset]['price'] = int(math.ceil(curr_price * 1.1))
    return assets


def update_grandma_rate(assets: AssetsDict) -> AssetsDict:
    '''
    Function calculates accrue rate for Grandma asset, given other assets
    '''
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
