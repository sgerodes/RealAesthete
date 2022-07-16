from ..persistence import models


class EbayKleinanzeigenParser:
    @staticmethod
    def create_from_scrapy_item(scrapy_item):
        db_model = models.EbayKleinanzeigen()

        db_model.price = scrapy_item.get('price')
        db_model.area = scrapy_item.get('area')
        db_model.postal_code = scrapy_item.get('postal_code')
        db_model.url = scrapy_item.get('url')
        db_model.exposition_type = scrapy_item.get('exposition_type')
        db_model.estate_type = scrapy_item.get('estate_type')

        db_model.source_id = scrapy_item.get('source_id')
        db_model.rooms = scrapy_item.get('rooms')
        db_model.city = scrapy_item.get('city')
        db_model.online_since = scrapy_item.get('online_since')

        return db_model


class ImmonetParser:
    @staticmethod
    def create_from_scrapy_item(scrapy_item):
        db_model = models.Immonet()

        db_model.price = scrapy_item.get('price')
        db_model.area = scrapy_item.get('area')
        db_model.postal_code = scrapy_item.get('postal_code')
        db_model.url = scrapy_item.get('url')
        db_model.exposition_type = scrapy_item.get('exposition_type')
        db_model.estate_type = scrapy_item.get('estate_type')

        db_model.source_id = scrapy_item.get('source_id')
        db_model.rooms = scrapy_item.get('rooms')
        db_model.city = scrapy_item.get('city')
        db_model.foreclosure = scrapy_item.get('foreclosure')

        return db_model




