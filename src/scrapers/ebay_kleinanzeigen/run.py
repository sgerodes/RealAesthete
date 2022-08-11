import os
import logging
from .ebay_kleinanzeigen.spiders.ebay import EbayFlatRentSpider, EbayFlatBuySpider, EbayHouseRentSpider, EbayHouseBuySpider
from .ebay_kleinanzeigen import settings
from scrapy.utils.project import get_project_settings
from ..utils import run_parallel_spiders


logger = logging.getLogger(__name__)


def run_spider():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings.__name__)
    spiders = (EbayFlatRentSpider, EbayFlatBuySpider, EbayHouseRentSpider, EbayHouseBuySpider)
    run_parallel_spiders(spiders=spiders, project_settings=get_project_settings())


def get_spider_and_settings():
    spiders = (EbayFlatRentSpider, EbayFlatBuySpider, EbayHouseRentSpider, EbayHouseBuySpider)

    logger.debug(f'Loading {settings.__name__=}')
    os.environ['SCRAPY_SETTINGS_MODULE'] = settings.__name__
    project_settings = get_project_settings()
    logger.debug(f'{project_settings["ITEM_PIPELINES"]._to_dict()=}')
    del os.environ['SCRAPY_SETTINGS_MODULE']
    return [(s, project_settings) for s in spiders]
