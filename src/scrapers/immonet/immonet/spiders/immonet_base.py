import scrapy
import logging
from ..items import ImmonetItem
from ....headers import get_random_header_set
from fake_useragent import UserAgent
import re
import datetime
from typing import List, Callable


logger = logging.getLogger(__name__)


def catch_errors(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f'Error occurred while executing function "{func.__name__}" with {args=}, {kwargs=}')
            logger.exception(e)
            return None
    return wrapper


class ImmonetSpider:
    BASE_URL = 'https://www.immonet.de/'

    def start_requests(self):
        ua = UserAgent()
        headers = get_random_header_set()
        headers["User-Agent"] = ua.random
        yield scrapy.http.Request(self.start_urls[0], headers=headers)

    @staticmethod
    @catch_errors
    def parse_item_id(text):
        return text.split('_')[1]

    def parse(self, response, **kwargs):
        logger.debug(f'Spider {self.__class__.__name__}: parsing url {response.request.url}')
        css_index_selector = '.item'
        next_page_css_selector = '.text-right'


        for elem in response.css(css_index_selector):
            source_id = self.parse_item_id(elem.xpath("@id").get())
            logger.debug(f'processing item with {source_id=}')

            item = ImmonetItem()
            item['source_id'] = source_id

            if hasattr(self, 'estate_type'):
                item['estate_type'] = self.estate_type
            if hasattr(self, 'exposition_type'):
                item['exposition_type'] = self.exposition_type
            if hasattr(self, 'foreclosure'):
                item['foreclosure'] = self.foreclosure

            yield item

        next_page_selector = response.css(next_page_css_selector)
        if next_page_selector:
            href = next_page_selector.xpath('@href').get()
            if href:
                next_page_url = f'{self.BASE_URL}{href}'
                logger.debug(f'Spider {self.__class__.__name__}: going to the next page {next_page_url}')
                yield scrapy.Request(next_page_url, callback=self.parse)
            else:
                logger.debug(f'Spider  {self.__class__.__name__}: href not found in the next_page_selector')