import scrapy
import logging
from ..items import EbayKleinanzeigenItem
from ..headers import get_random_header_set
from fake_useragent import UserAgent


logger = logging.getLogger(__name__)


class ProxySpider():
    start_urls = [
        "https://www.ebay-kleinanzeigen.de/s-immobilien/c195",
        # "https://httpbin.org/headers"
        # "https://free-proxy-list.net/"
        #        "https://api.myip.com/"
        #        "http://ip-api.com/json/"
        # "https://api.ipify.org?format=json"
    ]

    def start_requests(self):
        ua = UserAgent()
        headers = get_random_header_set()
        headers["User-Agent"] = ua.random
        yield scrapy.http.Request(self.start_urls[0], headers=headers)

    def parse_head(self, response, **kwargs):
        item = EbayKleinanzeigenItem()
        item['source_id'] = response.text
        yield item

    def parse_(self, response, **kwargs):
        item = EbayKleinanzeigenItem()
        item['source_id'] = response.text
        yield item

    def parse_free_prox(self, response, **kwargs):
        css_selector = "#list td:nth-child(2) , #list td:nth-child(1)"
        # css_selector = "td:nth-child(2) , td:nth-child(1)"
        xpath_selector = '//*[(@id = "list")]//td[(((count(preceding-sibling::*) + 1) = 2) and parent::*)] | //*[(@id = "list")]//td[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]'
        it = iter(response.css(css_selector).getall())
        # it = iter(response.xpath(xpath_selector + '/text()').getall())
        for elem in it:
            item = EbayKleinanzeigenItem()
            item['source_id'] = f'{elem}:{next(it)}'
            yield item
