import os
from .ebay_kleinanzeigen.spiders.ebay import EbayFlatRentSpider, EbayFlatBuySpider, EbayHouseRentSpider, EbayHouseBuySpider
from .ebay_kleinanzeigen import settings
from scrapy.utils.project import get_project_settings
from ..utils import run_parallel_spiders


def run_spider():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings.__name__)
    spiders = (EbayFlatRentSpider, EbayFlatBuySpider, EbayHouseRentSpider, EbayHouseBuySpider)
    # spiders = (EbayFlatRentSpider, )
    run_parallel_spiders(spiders=spiders, project_settings=get_project_settings())
