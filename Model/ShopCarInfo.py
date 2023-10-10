from dataclasses import dataclass

@dataclass
class ShopCarInfo:
    """Class to store car info from shopcar.com.br table"""
    carName: str
    tableInfo: dict
    price: float

    