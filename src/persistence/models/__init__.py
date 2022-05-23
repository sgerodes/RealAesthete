from .base import Base, engine
from .ebay_kleinanzeigen import EbayKleinanzeigen


def create_tables():
    Base.metadata.create_all(engine)


create_tables()
