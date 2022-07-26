from ..persistence import models
from ..scrapers.immowelt.immowelt.items import ImmoweltItem
from . import utils


class EbayKleinanzeigenParser:
    @staticmethod
    def create_from_scrapy_item(scrapy_item) -> models.EbayKleinanzeigen:
        db_model = utils.copy_all_properties_from_scrapy_item(scrapy_item, models.EbayKleinanzeigen())
        return db_model


class ImmonetParser:
    @staticmethod
    def create_from_scrapy_item(scrapy_item):
        db_model = utils.copy_all_properties_from_scrapy_item(scrapy_item, models.Immonet())
        return db_model


class ImmoweltParser:
    @staticmethod
    def create_from_scrapy_item(scrapy_item: ImmoweltItem):
        db_model = utils.copy_all_properties_from_scrapy_item(scrapy_item, models.Immowelt())
        return db_model
