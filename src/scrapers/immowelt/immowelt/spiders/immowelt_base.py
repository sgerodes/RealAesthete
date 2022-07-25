import scrapy
import logging
from ..items import *
from ....headers import get_random_header_set
from fake_useragent import UserAgent
from src import persistence
import re
import datetime
from typing import List, Callable
import datetime
import random
from ..items import ImmoweltItem
from scrapy.exceptions import CloseSpider


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


class ImmoweltSpider:
    BASE_URL = 'https://www.immowelt.de/'
    ABSOLUTE_TIMEDELTA_THRESHOLD = datetime.timedelta(days=7)
    RANDOM_DECLINE_RATE = 0.4
    ONE_DAY_TIMEDELTA = datetime.timedelta(days=1)

    @staticmethod
    @catch_errors
    def parse_source_id(item_css_selector):
        return item_css_selector.css('a::attr(id)').get()

    @staticmethod
    @catch_errors
    def parse_price(item_css_selector) -> float:
        text: str = item_css_selector.css('[data-test="price"]::text').get()
        return float(text.replace('€', '').replace('.', '').replace(',', '.').strip())

    @staticmethod
    @catch_errors
    def parse_area(item_css_selector) -> float:
        text: str = item_css_selector.css('[data-test="area"]::text').get()
        return float(text.replace('m²', '').strip())

    @staticmethod
    @catch_errors
    def parse_rooms(item_css_selector) -> float:
        text: str = item_css_selector.css('[data-test="rooms"]::text').get()
        return float(text.replace('Zi.', '').strip())

    @staticmethod
    @catch_errors
    def parse_city(item_css_selector) -> str:
        text: str = item_css_selector.css("[class^='IconFact']").css('span::text').get()
        return text

    def start_requests(self):
        ua = UserAgent()
        headers = {} # get_random_header_set()
        headers["User-Agent"] = ua.random
        # all = persistence.ImmoweltPostalCodeStatisticsRepository.read_all(estate_type=self.estate_type,
        #                                                                   exposition_type=self.exposition_type)
        all = persistence.ImmoweltPostalCodeStatisticsRepository.read_all(estate_type=self.estate_type,
                                                                          exposition_type=self.exposition_type)
        random.shuffle(all)
        for ipcs in all:
            should_search = False

            delta_since_last_search: datetime.timedelta = datetime.datetime.utcnow() - ipcs.last_search if ipcs.last_search else None
            if not delta_since_last_search or delta_since_last_search > self.ABSOLUTE_TIMEDELTA_THRESHOLD:
                if random.random() > self.RANDOM_DECLINE_RATE:
                    logger.debug('Will crawl, too much time passed since last search')
                    should_search = True
                else:
                    logger.debug('Will not crawl, because of the random decline rule')
                    continue

            delta_since_created: datetime.timedelta = datetime.datetime.utcnow() - ipcs.created_at
            frequency: datetime.timedelta = delta_since_created / ipcs.total_entries if ipcs.total_entries != 0 else datetime.timedelta(weeks=10000)
            # if not should_search and frequency < self.ONE_DAY_TIMEDELTA:
            #     logger.debug('Will crawl, because of frequency very high')
            #     should_search = True

            if not should_search and delta_since_last_search > frequency:
                logger.debug('Will crawl, because of frequency')
                should_search = True

            if should_search:
                url = self.start_urls[0].format(postal_code=ipcs.postal_code, page=1)
                yield scrapy.http.Request(url, headers=headers, cb_kwargs={'postal_code': ipcs.postal_code, 'page': 1})
            else:
                logger.debug('Will not search')

    def parse(self, response, postal_code: str, page: int):
        logger.debug(f'Spider {self.__class__.__name__}: parsing url {response.request.url}')

        css_index_selector = "[class^='EstateItem']"

        if response.status == 404:
            logger.warning(f'Request for {postal_code=} is 404. {response.request.url=}')

        elements_selector = response.css(css_index_selector)

        if response.css('body'):
            # This means we got blocked
            ipcs = persistence.ImmoweltPostalCodeStatisticsRepository.read_by_unique(estate_type=self.estate_type,
                                                                                     exposition_type=self.exposition_type,
                                                                                     postal_code=postal_code)
            ipcs.last_search = datetime.datetime.utcnow()
            persistence.ImmoweltPostalCodeStatisticsRepository.update(ipcs)
        else:
            logger.error(f'No body tag. We are probably blocked. {response.body=}')
            CloseSpider('No body tag. We are probably blocked.')

        for elem in elements_selector:
            item = ImmoweltItem()
            item.source_id = self.parse_source_id(elem)
            item.price = self.parse_price(elem)
            item.area = self.parse_area(elem)
            item.rooms = self.parse_rooms(elem)
            item.postal_code = postal_code
            item.city = self.parse_city(elem)
            if hasattr(self, 'estate_type'):
                item.estate_type = self.estate_type
            if hasattr(self, 'exposition_type'):
                item.exposition_type = self.exposition_type
            yield item

        if len(elements_selector) != 0:
            new_page = page + 1
            next_page_url = self.start_urls[0].format(postal_code=postal_code, page=new_page)
            logger.debug(f'Spider {self.__class__.__name__}: going to the next page {next_page_url}')
            yield scrapy.Request(next_page_url, callback=self.parse, cb_kwargs={'postal_code': postal_code, 'page': new_page})
        else:
            logger.debug('No elements found on the page')
