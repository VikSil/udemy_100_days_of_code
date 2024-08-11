from typing import List

from custom_types import AssetsDict
from calc_utils import refresh_theo_price, update_grandma_rate


def precalculate_strategy1(time: int, accrue_rate: float, assets: AssetsDict) -> List[str]:
    '''
    Function implements the naive approach of buying the highest yielding asset
    that we have enough cookies to acquire with a pre-calculated sequence of acquisitions

    Over 5 minutes of runtime we end up with approx.
    35 - Cursors
    17 - GrandMas
    1 - Factories
    0 - Mines
    28 - cookie rate
    '''
    asset_chain = []

    assets = dict(sorted(assets.items(), key=lambda item: item[1]['price']))
    next_asset = list(assets.keys())[0]
    next_price = assets[next_asset]['price']
    accrue_time = next_price / accrue_rate
    remaining_time = time - accrue_time

    if remaining_time > 0:
        assets[next_asset]['owned'] += 1
        assets = refresh_theo_price(next_asset, assets)
        assets = update_grandma_rate(assets)
        accrue_rate += assets[next_asset]['rate']
        chain_tail = precalculate_strategy1(remaining_time, accrue_rate, assets)
        asset_chain.append(next_asset)
        asset_chain = asset_chain + chain_tail
        return asset_chain
    else:
        # append one more than necessary, just in case
        asset_chain.append(next_asset)
        return asset_chain
