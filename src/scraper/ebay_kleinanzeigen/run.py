from .ebay_kleinanzeigen.spiders.ebay import EbayFlatRentSpider, EbayHouseRentSpider, EbayFlatSellSpider, EbayHouseSellSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import inspect


def run_spider():
    spider = EbayFlatSellSpider
    spider_module_name = inspect.getmodule(spider).__name__
    # 'src.scraper.ebay_kleinanzeigen.ebay_kleinanzeigen.spiders.ebay'
    settings_file_path = '.'.join(spider_module_name.split('.')[:-2]) + '.settings'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
    process.start()
