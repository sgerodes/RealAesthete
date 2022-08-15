import scrapy
import logging
from .ebay_base import EbayKleinanzeigenSpider
from ....enums import ExpositionType, EstateType


logger = logging.getLogger(__name__)


class EbayFlatRentSpider(EbayKleinanzeigenSpider):
    start_urls = [
         "https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/anzeige:angebote/seite:1/c203",
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.RENT


class EbayFlatBuySpider(EbayKleinanzeigenSpider):
    start_urls = [
        "https://www.ebay-kleinanzeigen.de/s-wohnung-kaufen/anzeige:angebote/c196"
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.BUY


class EbayHouseRentSpider(EbayKleinanzeigenSpider, scrapy.Spider):
    start_urls = [
         "https://www.ebay-kleinanzeigen.de/s-haus-mieten/anzeige:angebote/c205",
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.RENT


class EbayHouseBuySpider(EbayKleinanzeigenSpider, scrapy.Spider):
    start_urls = [
        "https://www.ebay-kleinanzeigen.de/s-haus-kaufen/anzeige:angebote/c208"
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.BUY


