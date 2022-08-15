import scrapy
import logging
from .immowelt_base import ImmoweltSpider
from ....enums import ExpositionType, EstateType


logger = logging.getLogger(__name__)


class ImmoweltFlatRentSpider(ImmoweltSpider):
    start_urls = [
         "https://www.immowelt.de/liste/{postal_code}/wohnungen/mieten?d=true&sd=DESC&sf=TIMESTAMP&sp={page}",
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.RENT


class ImmoweltFlatBuySpider(ImmoweltSpider):
    start_urls = [
        "https://www.immowelt.de/liste/{postal_code}/wohnungen/kaufen?d=true&sd=DESC&sf=TIMESTAMP&sp={page}"
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.BUY


class ImmoweltHouseRentSpider(ImmoweltSpider):
    start_urls = [
         "https://www.immowelt.de/liste/{postal_code}/haeuser/mieten?d=true&sd=DESC&sf=TIMESTAMP&sp={page}",
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.RENT


class ImmoweltHouseBuySpider(ImmoweltSpider):
    start_urls = [
        "https://www.immowelt.de/liste/{postal_code}/haeuser/kaufen?d=true&sd=DESC&sf=TIMESTAMP&sp={page}"
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.BUY
