import os
from .immowelt.spiders.immowelt import ImmoweltFlatRentSpider, ImmoweltFlatBuySpider, ImmoweltHouseRentSpider, ImmoweltHouseBuySpider
from .immowelt import settings
from scrapy.utils.project import get_project_settings
from ..utils import run_parallel_spiders


def run_spider():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings.__name__)
    #spiders = (ImmoweltFlatRentSpider, ImmoweltFlatBuySpider, ImmoweltHouseRentSpider, ImmoweltHouseBuySpider)
    spiders = (ImmoweltFlatBuySpider, )
    run_parallel_spiders(spiders=spiders, project_settings=get_project_settings())
