from enum import Enum


class EstateSource(Enum):
    EbayKleinanzeigen = 'EbayKleinanzeigen'


class ExpositionType(Enum):
    RENT = "RENT"
    SELL = "SELL"


class EstateType(Enum):
    HOUSE = "HOUSE"
    FLAT = "FLAT"
