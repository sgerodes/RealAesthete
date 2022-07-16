from ..persistence import models



class EbayKleinanzeigenParser:
    @staticmethod
    def create_from_scrapy_item(self, scrapy_item):
        ebay_kleinanzeigen = models.EbayKleinanzeigen()

        self.price = scrapy_item.get('price')
        self.area = scrapy_item.get('area')
        self.postal_code = scrapy_item.get('postal_code')
        self.url = scrapy_item.get('url')
        self.exposition_type = scrapy_item.get('exposition_type')
        self.estate_type = scrapy_item.get('estate_type')

        self.source_id = scrapy_item.get('source_id')
        self.rooms = scrapy_item.get('rooms')
        self.city = scrapy_item.get('city')
        self.online_since = scrapy_item.get('online_since')

        return ebay_kleinanzeigen
