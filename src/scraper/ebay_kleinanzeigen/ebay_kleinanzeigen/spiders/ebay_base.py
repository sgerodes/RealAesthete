import scrapy
import logging
from ..items import EbayKleinanzeigenItem
from ..headers import get_random_header_set
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


class EbayKleinanzeigenSpider:
    BASE_URL = 'https://www.ebay-kleinanzeigen.de'

    def start_requests(self):
        ua = UserAgent()
        headers = get_random_header_set()
        headers["User-Agent"] = ua.random
        yield scrapy.http.Request(self.start_urls[0], headers=headers)

    @staticmethod
    @catch_errors
    def parse_price(text: str):
        # example: '\n                                        7.500 €'
        if not text or '€' not in text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.')
        return None

    @staticmethod
    @catch_errors
    def parse_area(text: str):
        # example: '175 m²'
        if not text or 'm²' not in text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.')
        return None

    @staticmethod
    @catch_errors
    def parse_rooms(text: str):
        # example: '9 Zimmer'
        if not text or 'Zimmer' not in text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.')
        return None

    @staticmethod
    @catch_errors
    def parse_postal_code_and_city(text: str):
        # example: ' 59602 Rüthen'
        if not text:
            return None, None
        split: list = text.strip().split(' ', 1)
        if len(split) != 2:
            logger.debug(f'Could not split the postal code and city text into two parts. Got {len(split)}')
            return None, None
        postal_code, city = split
        return postal_code, city

    @staticmethod
    @catch_errors
    def parse_online_since(text: str):
        # example ' Heute, 21:38'
        text = text.strip()
        if not text:
            return None
        if "Heute" in text:
            d = datetime.date.today()
            t_str = text.split(",")[1].strip()
            t = datetime.time.fromisoformat(t_str)
            return datetime.datetime.combine(d, t)
        elif "Gestern" in text:
            d = datetime.datetime.now() - datetime.timedelta(1)
            t_str = text.split(",")[1].strip()
            t = datetime.time.fromisoformat(t_str)
            return datetime.datetime.combine(d, t)
        else:
            return datetime.date.fromisoformat(text.replace(".", "-"))

    @staticmethod
    @catch_errors
    def scalp_tags(item, tags: List[str]):
        for tag in tags:
            if 'Zimmer' in tag:
                item['rooms'] = EbayKleinanzeigenSpider.parse_rooms(tag)
            if 'm²' in tag:
                item['area'] = EbayKleinanzeigenSpider.parse_area(tag)

    def parse(self, response, **kwargs):
        logger.debug(f'Spider {self.__class__.__name__}: parsing url {response.request.url}')
        css_index_selector = '.aditem'
        next_page_css_selector = '.pagination-next'

        for elem in response.css(css_index_selector):
            source_id = elem.xpath("@data-adid").get()
            logger.debug(f'processing item with {source_id=}')

            item = EbayKleinanzeigenItem()
            item['source_id'] = source_id
            item['url'] = elem.xpath("@data-href").get()
            item['price'] = self.parse_price(elem.css('.aditem-main--middle--price::text').get())
            item['postal_code'], item['city'] = self.parse_postal_code_and_city(''.join(elem.css('.aditem-main--top--left::text').getall()))
            item['online_since'] = self.parse_online_since(''.join(elem.css('.aditem-main--top--right::text').getall()))
            self.scalp_tags(item, elem.css('.simpletag::text').getall())

            if hasattr(self, 'estate_type'):
                item['estate_type'] = self.estate_type
            if hasattr(self, 'exposition_type'):
                item['exposition_type'] = self.exposition_type

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