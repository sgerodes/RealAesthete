from .base import Estate, Base, EstateSource
from sqlalchemy import Column, Integer, String, Float, Numeric, DateTime
from ...scraper.ebay_kleinanzeigen.ebay_kleinanzeigen.items import EbayKleinanzeigenItem


class EbayKleinanzeigen(Base, Estate):
    __tablename__ = 'EbayKleinanzeigen'

    def __init__(self, from_scrapy_item: EbayKleinanzeigenItem):
        self.source = EstateSource.EbayKleinanzeigen
        if from_scrapy_item:
            self.copy_scrapy_fields(from_scrapy_item)

    source_id = Column(String)
    rooms = Column(Float)
    city = Column(String)
    online_since = Column(DateTime(timezone=True))

    def copy_scrapy_fields(self, item: EbayKleinanzeigenItem):
        self.price = item.get('price')
        self.area = item.get('area')
        self.postal_code = item.get('postal_code')
        self.url = item.get('url')
        self.exposition_type = item.get('exposition_type')
        self.estate_type = item.get('estate_type')

        self.source_id = item.get('source_id')
        self.rooms = item.get('rooms')
        self.city = item.get('city')
        self.online_since = item.get('online_since')
