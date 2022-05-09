from .base import Base, engine
from .ebay_kleinanzeigen import EbayKleinanzeigen

if __name__ == '__main__':
    Base.metadata.create_all(engine)
