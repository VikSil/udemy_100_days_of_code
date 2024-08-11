from typing import TypedDict


class DetailsDict(TypedDict):
    price: int
    owned: int
    rate: int


class AssetsDict(TypedDict):
    buyCursor: DetailsDict
    buyGrandma: DetailsDict
    buyFactory: DetailsDict
    BuyMine: DetailsDict
    buyShipment: DetailsDict


class NodeDict(TypedDict):
    hash_id: int
    parent_id: int
    side: str
    assets: AssetsDict
    purchase: str
    rate: float
    time: float
    terminal: bool
