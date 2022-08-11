import scrapy
import logging
from ..items import ImmonetItem
from ....headers import get_random_header_set
from fake_useragent import UserAgent
import re
import datetime
from src import persistence
from typing import List, Callable, Optional

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
            city = text.split('•')[1].strip()\
                .replace('\n', '')\
                .replace('\r', '')\
                .replace('\t\t\t\t\t\t\t', ' ')
            split = city.split(' ')
            if len(split) == 2 and split[0] == split[1]:
                city = split[0]
            return city
        return None

    @staticmethod
    @catch_errors
    def parse_rooms(text: str) -> Optional[float]:
        if text is None:
            return None
        # example: ' 3.5 '
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found
        return None

    @staticmethod
    @catch_errors
    def parse_area(text: str) -> Optional[float]:
        # example: ' 44 '
        if not text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found
        return None

    @staticmethod
    @catch_errors
    def parse_postal_code(text: str) -> Optional[float]:
        # example: ' 63636&nbsp; Brachttal '
        if not text:
            return None
        search = re.compile(r'\d{5}').search(text)
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
            item['city'] = self.parse_city(elem.css(".text-100:not(.no-image)::text").get())
            item['rooms'] = self.parse_rooms(elem.css("div[id*='selRooms_']").css('.text-nowrap::text').get())
            item['area'] = self.parse_area(elem.css("div[id*='selArea_']").css('.text-nowrap::text').get())

            if hasattr(self, 'estate_type'):
                item['estate_type'] = self.estate_type
            if hasattr(self, 'exposition_type'):
                item['exposition_type'] = self.exposition_type
            if hasattr(self, 'foreclosure'):
                item['foreclosure'] = self.foreclosure

            yield item
            yield scrapy.Request(f'https://www.immonet.de/angebot/{source_id}',
                                 callback=self.parse_detailed_page,
                                 cb_kwargs={'source_id': source_id})

        next_page_selector = response.css(next_page_css_selector)
        if next_page_selector:
            href = next_page_selector.xpath('@href').get()
            if href:
                next_page_url = f'{self.BASE_URL}{href}'
                logger.debug(f'Spider {self.__class__.__name__}: going to the next page {next_page_url}')
                yield scrapy.Request(next_page_url, callback=self.parse)
            else:
                logger.debug(f'Spider  {self.__class__.__name__}: href not found in the next_page_selector')

    def parse_detailed_page(self, response, source_id: str, **kwargs):
        logger.debug(f'Scraping detailed {source_id=}')
        immonet = persistence.ImmonetRepository.read_by_source_id(source_id)
        if not immonet:
            logger.error(f'Scrapy detailed page for {source_id=}, but no corresponding db model was found')
            return None

        postal_code = self.parse_postal_code(response.css('.show').css('.text-100.pull-left::text').get())
        immonet.postal_code = postal_code
        persistence.ImmonetRepository.update(immonet)
