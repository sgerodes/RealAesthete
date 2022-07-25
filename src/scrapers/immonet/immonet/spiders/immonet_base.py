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
            logger.warning(f'Error occurred while executing function "{func.__name__}" with args={args}, kwargs={kwargs}')
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
    def parse_price(text: str):
        # example: '1.040 '
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.').replace('€', '')
        return None

    @staticmethod
    @catch_errors
    def parse_city(text: str):
        # example: 'Etagenwohnung • Coswig '
        if text:
            return text.split('•')[1].strip().replace('\n', '').replace('\r', '')
        return None

    @staticmethod
    @catch_errors
    def parse_rooms(text: str):
        # example: ' 3.5 '
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found
        return None

    @staticmethod
    @catch_errors
    def parse_area(text: str):
        # example: ' 44 '
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found
        return None

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
            logger.debug(f'parsing item with source_id={source_id}')

            item = ImmonetItem()
            item['source_id'] = source_id
            item['price'] = self.parse_price(elem.css("div[id*='selPrice_']").css('.text-nowrap::text').get())
            item['city'] = self.parse_city(elem.css(".text-100::text").get())
            item['rooms'] = self.parse_rooms(elem.css("div[id*='selRooms_']").css('.text-nowrap::text').get())
            item['area'] = self.parse_area(elem.css("div[id*='selArea_']").css('.text-nowrap::text').get())

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