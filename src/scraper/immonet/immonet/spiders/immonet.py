import scrapy
import logging
from .immonet_base import ImmonetSpider
from ....enums import ExpositionType, EstateType


logger = logging.getLogger(__name__)


class ImmonetFlatRentSpider(ImmonetSpider, scrapy.Spider):
    name = 'EbayFlatRentSpider'
    start_urls = [
         "https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&objecttype=1&listsize=26&locationname=&acid=&actype=&ajaxIsRadiusActive=true&sortby=19&suchart=1&radius=0&pcatmtypes=1_2&pCatMTypeStoragefield=&parentcat=1&marketingtype=2&fromprice=&toprice=&fromarea=&toarea=&fromrooms=&torooms=&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen",
    ]
    estate_type = EstateType.FLAT
    exposition_type = ExpositionType.RENT

