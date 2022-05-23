import scrapy
import logging
from ..items import EbayKleinanzeigenItem
from ..headers import get_random_header_set
from fake_useragent import UserAgent
import re
import datetime
from typing import List

logger = logging.getLogger(__name__)


class EbayKleinanzeigenSpider:

    def start_requests(self):
        ua = UserAgent()
        headers = get_random_header_set()
        headers["User-Agent"] = ua.random
        yield scrapy.http.Request(self.start_urls[0], headers=headers)

    @staticmethod
    def parse_price(text):
        # example: '\n                                        7.500 €'
        if not text or '€' not in text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.')
        return None

    @staticmethod
    def parse_area(text):
        # example: '175 m²'
        if not text or 'm²' not in text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.')
        return None

    @staticmethod
    def parse_rooms(text):
        # example: '9 Zimmer'
        if not text or 'Zimmer' not in text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.')
        return None

    @staticmethod
    def parse_postal_code_and_city(text):
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
    def parse_online_since(text):
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

    def scalp_tags(self, item, tags: List[str]):
        for tag in tags:
            if 'Zimmer' in tag:
                item['rooms'] = self.parse_rooms(tag)
            if 'm²' in tag:
                item['area'] = self.parse_area(tag)

    def parse(self, response, **kwargs):
        css_index_selector = '.aditem'

        for elem in response.css(css_index_selector):
            item = EbayKleinanzeigenItem()
            item['source_id'] = elem.xpath("@data-adid").get()
            logger.debug(f'processing item with source_id={item.get("source_id")}')
            item['url'] = elem.xpath("@data-href").get()
            item['price'] = self.parse_price(elem.css('.aditem-main--middle--price::text').get())

            self.scalp_tags(item, elem.css('.simpletag::text').getall())

            item['postal_code'], item['city'] = self.parse_postal_code_and_city(''.join(elem.css('.aditem-main--top--left::text').getall()))

            item['online_since'] = self.parse_online_since(''.join(elem.css('.aditem-main--top--right::text').getall()))

            yield item
