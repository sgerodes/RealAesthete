import scrapy
import logging
from .ebay_base import EbayKleinanzeigenSpider
from ..enums import ExpositionType, EstateType


logger = logging.getLogger(__name__)


class EbayHouseRentSpider(EbayKleinanzeigenSpider, scrapy.Spider):
    name = 'EbayHouseRentSpider'
    start_urls = [
         "https://www.ebay-kleinanzeigen.de/s-haus-mieten/c205",
    ]

    def parse(self, response, **kwargs):
        for item in super().parse(response, **kwargs):
            item['estate_type'] = EstateType.HOUSE
            item['exposition_type'] = ExpositionType.RENT
            yield item
