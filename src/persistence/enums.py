import enum


class EstateSource(enum.Enum):
    EbayKleinanzeigen = 'EbayKleinanzeigen'
    Immonet = 'Immonet'
    Immowelt = 'Immowelt'


class EnergyEfficiencyClass(enum.Enum):
    A_PLUS = 'A+'
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    F = 'F'
    G = 'G'
    H = 'H'
