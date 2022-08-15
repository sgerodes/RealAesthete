import scrapy
import logging
from .immonet_base import ImmonetSpider, ImmonetPostalCodeSpider, AbstractImmonetForeclosureSpider
from ....enums import ExpositionType, EstateType


logger = logging.getLogger(__name__)


class ImmonetFlatRentSpider(ImmonetSpider):
    start_urls = [
         "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=1_2&pCatMTypeStoragefield=&parentcat=1&marketingtype=2&fromprice=&toprice=&fromarea=&toarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen",
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.RENT


class ImmonetFlatBuySpider(ImmonetSpider):
    start_urls = [
        "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=1_1&pCatMTypeStoragefield=1_6&parentcat=1&marketingtype=1&fromprice=&toprice=&fromarea=&toarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen"
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.BUY


class ImmonetHouseRentSpider(ImmonetSpider):
    start_urls = [
         "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=2_2&pCatMTypeStoragefield=1_1&parentcat=2&marketingtype=2&fromprice=&toprice=&fromarea=&toarea=&fromplotarea=&toplotarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen",
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.RENT


class ImmonetHouseBuySpider(ImmonetSpider):
    start_urls = [
        "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=2_1&pCatMTypeStoragefield=2_2&parentcat=2&marketingtype=1&fromprice=&toprice=&fromarea=&toarea=&fromplotarea=&toplotarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen"
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.BUY


# Foreclosure == Zwangsversteigerung
class ImmonetFlatForeclosureSpider(AbstractImmonetForeclosureSpider):
    start_urls = [
        "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=1_6&pCatMTypeStoragefield=2_6&parentcat=1&marketingtype=6&fromprice=&toprice=&fromarea=&toarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen"
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.BUY
    foreclosure = True


class ImmonetHouseForeclosureSpider(AbstractImmonetForeclosureSpider):
    start_urls = [
        "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=2_6&pCatMTypeStoragefield=2_1&parentcat=2&marketingtype=6&fromprice=&toprice=&fromarea=&toarea=&fromplotarea=&toplotarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen"
    ]
    estate_type = EstateType.HOUSE
    exposition_type = ExpositionType.BUY
    foreclosure = True
