import scrapy
import logging
from .immowelt_base import ImmoweltSpider
from ....enums import ExpositionType, EstateType


logger = logging.getLogger(__name__)


class ImmoweltFlatRentSpider(ImmoweltSpider, scrapy.Spider):
    name = 'ImmonetFlatRentSpider'
    start_urls = [
         "https://www.immowelt.de/liste/{zip_code}/wohnungen/mieten?d=true&sd=DESC&sf=TIMESTAMP&sp=1",
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.RENT


class ImmoweltFlatBuySpider(ImmoweltSpider, scrapy.Spider):
    name = 'ImmonetFlatBuySpider'
    start_urls = [
        "https://www.immowelt.de/liste/{zip_code}/wohnungen/kaufen?d=true&sd=DESC&sf=TIMESTAMP&sp=1"
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.BUY


class ImmoweltHouseRentSpider(ImmoweltSpider, scrapy.Spider):
    name = 'ImmonetHouseRentSpider'
    start_urls = [
         "https://www.immowelt.de/liste/{zip_code}/haeuser/mieten?d=true&sd=DESC&sf=TIMESTAMP&sp=1",
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.RENT


class ImmoweltHouseBuySpider(ImmoweltSpider, scrapy.Spider):
    name = 'ImmonetHouseBuySpider'
    start_urls = [
        "https://www.immowelt.de/liste/{zip_code}/haeuser/kaufen?d=true&sd=DESC&sf=TIMESTAMP&sp=1"
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.BUY
