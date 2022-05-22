import scrapy
import logging
from .ebay_base import EbayKleinanzeigenSpider
from ..enums import ExpositionType, EstateType


logger = logging.getLogger(__name__)


class EbayFlatRentSpider(EbayKleinanzeigenSpider, scrapy.Spider):
    name = 'EbayFlatRentSpider'
    start_urls = [
         "https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/c203",
    ]

    def parse(self, response, **kwargs):
        for item in super().parse(response, **kwargs):
            item['estate_type'] = EstateType.FLAT
            item['exposition_type'] = ExpositionType.RENT
            yield item
