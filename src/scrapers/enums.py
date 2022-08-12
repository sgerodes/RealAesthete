from enum import Enum


class ExpositionType(Enum):
    RENT = "RENT"
    BUY = "BUY"


class EstateType(Enum):
    HOUSE = "HOUSE"
    FLAT = "FLAT"


class PersistencePipelineStats(Enum):
    READING = "READING"
    CREATION = "CREATION"
