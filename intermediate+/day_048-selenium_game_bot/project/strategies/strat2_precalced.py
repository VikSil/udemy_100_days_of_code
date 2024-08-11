import math
from typing import List

from custom_types import AssetsDict
from calc_utils import find_best_roi, refresh_theo_price, update_grandma_rate


def precalculate_strategy2(time: float, accrue_rate: float, assets: AssetsDict) -> List[str]:
    '''
    Function implements a strategy of waiting to accrue enough cookies
    to acquire the asset with the highest ROI with a pre-calculated sequence of acquisitions

    Over 5 minutes of runtime we end up with approx.
    21 - Cursors
    15 - GrandMas
    9 - Factories
    4 - Mines
    101.2 - cookie rate
    '''
    asset_chain = []
    next_asset = find_best_roi(assets)
    next_price = assets[next_asset]['price']
    accrue_time = int(math.ceil(next_price / accrue_rate))
    remaining_time = int(math.ceil(time - accrue_time))

    if remaining_time > 0:
        assets[next_asset]['owned'] += 1
        assets = refresh_theo_price(next_asset, assets)
        assets = update_grandma_rate(assets)
        accrue_rate += assets[next_asset]['rate']
        chain_tail = precalculate_strategy2(remaining_time, accrue_rate, assets)
        asset_chain.append(next_asset)
        asset_chain = asset_chain + chain_tail
        return asset_chain
    else:
        # append one more than necessary, just in case
        asset_chain.append(next_asset)
        return asset_chain
