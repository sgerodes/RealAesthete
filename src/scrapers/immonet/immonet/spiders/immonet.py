import scrapy
import logging
from .immonet_base import ImmonetSpider
from ....enums import ExpositionType, EstateType


logger = logging.getLogger(__name__)


class ImmonetFlatRentSpider(ImmonetSpider, scrapy.Spider):
    name = 'ImmonetFlatRentSpider'
    start_urls = [
         "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=1_2&pCatMTypeStoragefield=&parentcat=1&marketingtype=2&fromprice=&toprice=&fromarea=&toarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen",
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.RENT


class ImmonetFlatBuySpider(ImmonetSpider, scrapy.Spider):
    name = 'ImmonetFlatBuySpider'
    start_urls = [
        "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=1_1&pCatMTypeStoragefield=1_6&parentcat=1&marketingtype=1&fromprice=&toprice=&fromarea=&toarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen"
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.BUY


class ImmonetHouseRentSpider(ImmonetSpider, scrapy.Spider):
    name = 'ImmonetHouseRentSpider'
    start_urls = [
         "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=2_2&pCatMTypeStoragefield=1_1&parentcat=2&marketingtype=2&fromprice=&toprice=&fromarea=&toarea=&fromplotarea=&toplotarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen",
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.RENT


class ImmonetHouseBuySpider(ImmonetSpider, scrapy.Spider):
    name = 'ImmonetHouseBuySpider'
    start_urls = [
        "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=2_1&pCatMTypeStoragefield=2_2&parentcat=2&marketingtype=1&fromprice=&toprice=&fromarea=&toarea=&fromplotarea=&toplotarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen"
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.BUY


# Foreclosure == Zwangsversteigerung
class ImmonetFlatForeclosureSpider(ImmonetSpider, scrapy.Spider):
    name = 'ImmonetFlatForeclosureSpider'
    start_urls = [
        "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=1_6&pCatMTypeStoragefield=2_6&parentcat=1&marketingtype=6&fromprice=&toprice=&fromarea=&toarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen"
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.BUY
    foreclosure = True


class ImmonetHouseForeclosureSpider(ImmonetSpider, scrapy.Spider):
    name = 'ImmonetHouseForeclosureSpider'
    start_urls = [
        "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=2_6&pCatMTypeStoragefield=2_1&parentcat=2&marketingtype=6&fromprice=&toprice=&fromarea=&toarea=&fromplotarea=&toplotarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen"
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.BUY
    foreclosure = True

