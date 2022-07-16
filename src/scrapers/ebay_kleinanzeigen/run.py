from .ebay_kleinanzeigen.spiders.ebay import EbayFlatRentSpider, EbayFlatBuySpider, EbayHouseRentSpider, EbayHouseBuySpider
from .ebay_kleinanzeigen import settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


def run_spider():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings.__name__)
    for spider in (EbayFlatRentSpider, ):
        process = CrawlerProcess(get_project_settings())
        process.crawl(spider)
        process.start()
