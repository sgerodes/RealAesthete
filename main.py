import configuration  # noinspection Do not delete
import logging
from src.scraper.ebay_kleinanzeigen.ebay_kleinanzeigen.spiders.ebay_flat_rent import EbayFlatRentSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


logger = logging.getLogger(__name__)


def main():
    # ek = persistence.models.EbayKleinanzeigen()
    # ek.price = 1230
    # ek.area = 23
    #persistence.service.save_estate_entity(ek)
    crawl_ebay()
    #ans = persistence.service.read_all_ebay_kleinanzeigen()
    #logger.debug(ans)


def crawl_ebay():
    logger.debug(f'Starting ebay crawler')
    process = CrawlerProcess(settings=get_project_settings())
    # process = CrawlerProcess()
    process.crawl(EbayFlatRentSpider)
    process.start()


if __name__ == '__main__':
    main()
