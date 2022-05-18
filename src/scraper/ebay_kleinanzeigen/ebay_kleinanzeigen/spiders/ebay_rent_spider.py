import scrapy
import logging
from ..items import EbayKleinanzeigenItem


logger = logging.getLogger(__name__)


class EbayRentSpider(scrapy.Spider):
    name = 'EbayRentSpider'
    start_urls = [
        "https://www.ebay-kleinanzeigen.de/s-immobilien/c195"
    ]

    def parse(self, response, **kwargs):
        css_index_selector = '.aditem::attr(data-adid)'
        #xpath_selector = '//*[contains(concat( " ", @class, " " ), concat( " ", "aditem", " " ))]'
        xpath_selector = "//*[contains(@class, 'aditem')]"

        #for elem in response.css(css_index_selector).getall():
        for elem in response.xpath(xpath_selector):
            item = EbayKleinanzeigenItem()
            item['source_id'] = elem.xpath("@data-adid").get() #.css('::attr(data-adid)')
            #  response.xpath("//*[contains(@class, 'aditem')]")[0].xpath("@data-adid").get()
            yield item
