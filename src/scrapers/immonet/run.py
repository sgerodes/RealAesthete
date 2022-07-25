import os
from .immonet.spiders.immonet import ImmonetFlatRentSpider, ImmonetFlatBuySpider, \
    ImmonetHouseRentSpider, ImmonetHouseBuySpider, ImmonetFlatForeclosureSpider, ImmonetHouseForeclosureSpider
from .immonet import settings
from scrapy.utils.project import get_project_settings
from ..utils import run_parallel_spiders


def run_spider():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings.__name__)
    spiders = (ImmonetFlatRentSpider, ImmonetFlatBuySpider, ImmonetHouseRentSpider, ImmonetHouseBuySpider,
                   ImmonetFlatForeclosureSpider, ImmonetHouseForeclosureSpider)
    run_parallel_spiders(spiders=spiders, project_settings=get_project_settings())


def get_spider_and_settings():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings.__name__)
    spiders = (ImmonetFlatRentSpider, ImmonetFlatBuySpider, ImmonetHouseRentSpider, ImmonetHouseBuySpider,
                   ImmonetFlatForeclosureSpider, ImmonetHouseForeclosureSpider)
    return [(s,get_project_settings()) for s in spiders]
