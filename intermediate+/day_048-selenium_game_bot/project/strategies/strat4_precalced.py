import copy
import math
from typing import List

from custom_types import AssetsDict, NodeDict
from calc_utils import find_best_roi_array, find_time_till_acquisition, refresh_theo_price, update_grandma_rate


def precalculate_strategy4(time: float, accrue_rate: float, assets: AssetsDict) -> List[str]:
    ''' '
    Function implements a recursive binary tree strategy.

    Each node contains state atributes:
        * id containing its level address
        * owned assets
        * last purchased asset
        * current rate - the weight distinguishing left node vs right node
        * remaining time
        * terminal node flag

    The tree is built following this algorythm:
    1) For each artifact calculate:
        * the ROI of the next acquisition
        * the time required to accrue the current price of the artifact
            * if accrual time higher than remaining time, the artifact is removed from consideration
                * if all arifacts are removed, the branch terminates
        * the ROI / time till acquisition - looking for highest
        * the time remaining after acquisition
        * the post-acquisition rate x time remaining - looking for highest
    2) If both (ROI / time till acquisition) and (post-acquisition rate x time remaining)
        are highest for the same asset - purchase that asset.
        Otherwise branch between the two assets with highest results.
        Assume that no cash is left over after acquisition.
    3) Recalculate for all nonterminated child nodes

    When all branches have been terminated, find the highest rate amongst all terminal nodes
    and build the sequence of purchased assets by tracing the path back to root

    The strategy is too memory heavy for 5 miunte runtime on my PC
    Over 2 minutes of runtime we end up with approx.
    11 - Cursors
    4 - GrandMas
    2 - Factories
    1 - Mines
    25.8 - cookie rate

    In all tests the precalculated time does not coincide with the actual runtime,
    rendering the solution False. After multiple attempts to fix the timing, I've given up on this exercise
    '''
    time = time * 0.7  # best koefiecient appears to be different for different timespans
    tree_root = {
        'parent_id': 0,
        'hash_id': hash(
            f"Parent: {0} Direction: {'X'} Purchase: {None}, Rate: {accrue_rate}, Remaining time: {time}, Terminal: {False} Assets: {assets}"
        ),
        'direction': 'X',
        'assets': assets,
        'purchase': None,
        'rate': accrue_rate,
        'time': time,
        'terminal': False,
    }

    print('Making Tree...')
    tree = make_tree(tree_root)
    print('Flattening the tree...')
    flat_tree = flatten_tree(tree)
    print('Looking for the terminal node...')
    terminal_node, terminal_index = find_best_terminal(flat_tree)
    expected_rate = (terminal_node['rate'] - accrue_rate) / 5
    print(f'Expected rate: {expected_rate}')
    flat_tree = flat_tree[:terminal_index]
    print('Searching for path...')
    path = find_path_to_root(terminal_node, flat_tree)
    print('Reducing to asset chain:')
    asset_chain = [purchase[1] for purchase in path if purchase[1] is not None]
    print(asset_chain)
    return asset_chain


def make_tree(root: NodeDict) -> List[List[NodeDict]]:
    '''
    Function calculates the binary tree of the strategy
    '''
    ROI_dict = find_best_roi_array(root['assets'])

    times_till_acquisition_dict = find_time_till_acquisition(root['assets'], root['rate'])
    times_till_acquisition_dict = {k: v for k, v in times_till_acquisition_dict.items() if v <= root['time']}

    if len(times_till_acquisition_dict) == 0:
        root['terminal'] = True
        tree = [root]

    else:
        tree = [root]
        weighted_ROI_dict = {k: ROI_dict[k] / v for k, v, in times_till_acquisition_dict.items()}
        max_ROI_asset = max(weighted_ROI_dict, key=weighted_ROI_dict.get)

        accrue_till_expiration_dict = {
            k: math.floor(((root['time'] - v) * root['assets'][k]['rate']))
            for k, v in times_till_acquisition_dict.items()
        }

        max_accrue_asset = max(accrue_till_expiration_dict, key=accrue_till_expiration_dict.get)

        # left node - buy the max ROI asset
        reduced_time_left = math.floor((root['time'] - times_till_acquisition_dict[max_ROI_asset]))

        left_node = compose_node(parent=root, purchase=max_ROI_asset, time=reduced_time_left, direction='L')
        tree.append(make_tree(left_node))

        # right node - buy max accrue asset, if different than the max ROI asset
        if max_ROI_asset != max_accrue_asset:

            reduced_time_right = math.floor((root['time'] - times_till_acquisition_dict[max_accrue_asset]))

            right_node = compose_node(parent=root, purchase=max_accrue_asset, time=reduced_time_right, direction='R')
            tree.append(make_tree(right_node))

    return tree


def compose_node(parent: NodeDict, purchase: str, time: float, direction: str) -> NodeDict:
    '''
    Function creates a node structure to pass as Left or Right child
    '''
    parent_hash = hash(
        f"Parent: {parent['parent_id']} Direction: {parent['direction']} Purchase: {parent['purchase']}, Rate: {parent['rate']}, Remaining time: {parent['time']}, Terminal: {parent['terminal']} Assets: {parent['assets']}"
    )

    assets = copy.deepcopy(parent['assets'])
    assets[purchase]['owned'] += 1
    assets = refresh_theo_price(purchase, assets)
    assets = update_grandma_rate(assets)

    rate = parent['rate'] + assets[purchase]['rate']

    node = {
        'parent_id': parent_hash,
        'hash_id': hash(
            f"Parent: {parent_hash} Direction: {direction} Purchase: {purchase}, Rate: {rate}, Remaining time: {time}, Terminal: {False} Assets: {assets}"
        ),
        'direction': direction,
        'assets': assets,
        'purchase': purchase,
        'rate': rate,
        'time': time,
        'terminal': False,
    }

    return node


def flatten_tree(tree: List[List[NodeDict]]) -> List[NodeDict]:
    '''
    Function flattens a list of lists into a single level list of nodes
    '''
    if tree == []:
        return tree
    if isinstance(tree[0], list):
        return flatten_tree(tree[0]) + flatten_tree(tree[1:])
    return tree[:1] + flatten_tree(tree[1:])


def find_best_terminal(nodes: List[NodeDict]) -> NodeDict:
    '''
    Function finds a terminal node with the greatest rate
    '''
    terminal_nodes = [(node, index) for index, node in enumerate(nodes) if node['terminal'] == True]
    best_terminal = max(terminal_nodes, key=lambda x: x[0]['rate'])
    return best_terminal[0], best_terminal[1]


def find_path_to_root(child_node: NodeDict, nodes: List[NodeDict]) -> List[str]:
    '''
    Function finds a path from a terminal node up to the root node
    '''
    path = [(child_node['hash_id'], child_node['purchase'])]
    parent_hash = child_node['parent_id']
    (parent_node, parent_node_index) = next(
        ((node, index) for index, node in enumerate(nodes) if node['hash_id'] == parent_hash), (None, None)
    )

    while parent_node is not None:
        nodes = nodes[:parent_node_index]
        child_node = parent_node
        path.insert(0, (child_node['hash_id'], child_node['purchase']))
        parent_hash = child_node['parent_id']
        (parent_node, parent_node_index) = next(
            ((node, index) for index, node in enumerate(nodes) if node['hash_id'] == parent_hash), (None, None)
        )

    return path
