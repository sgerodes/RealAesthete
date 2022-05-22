import scrapy
import logging
from .ebay_base import EbayKleinanzeigenSpider
from ..enums import ExpositionType, EstateType


logger = logging.getLogger(__name__)


class EbayHouseSellSpider(EbayKleinanzeigenSpider, scrapy.Spider):
    name = 'EbayHouseSellSpider'
    start_urls = [
        "https://www.ebay-kleinanzeigen.de/s-wohnung-kaufen/c196"
    ]

    def parse(self, response, **kwargs):
        for item in super().parse(response, **kwargs):
            item['estate_type'] = EstateType.FLAT
            item['exposition_type'] = ExpositionType.SELL
            yield item
