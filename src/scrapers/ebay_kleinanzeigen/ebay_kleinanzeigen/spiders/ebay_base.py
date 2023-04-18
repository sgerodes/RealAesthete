import scrapy
import logging
from ..items import EbayKleinanzeigenItem
from ....headers import get_random_header_set
from fake_useragent import UserAgent
import re
import datetime
from typing import List, Callable
from ....generic import BaseSpider
from src.scrapers.utils import catch_errors
from configuration.scrapy_configuration import EbayKleinanzeigenScrapingConfig as Config
import lxml


# logger = logging.getLogger(__name__)


class EbayKleinanzeigenSpider(BaseSpider):
    def start_requests(self):
        yield scrapy.http.Request(self.start_urls[0], headers=self.get_headers())

    @classmethod
    @catch_errors
    def parse_price(cls, text: str):
        # example: '\n                                        7.500 €'
        if not text or '€' not in text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.')
        return None

    @classmethod
    @catch_errors
    def parse_area(cls, text: str):
        # example: '175 m²'
        if not text or 'm²' not in text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.')
        return None

    @classmethod
    @catch_errors
    def parse_rooms(cls, text: str):
        # example: '9 Zimmer'
        if not text or 'Zimmer' not in text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.')
        return None

    @classmethod
    @catch_errors
    def parse_postal_code_and_city_from_div_tag(cls, tag_text: str):
        # example: ' <div class="aditem-main--top--left">
        #     <i class="icon icon-small icon-pin"></i> 79862 Höchenschwand
        # </div>'
        root = lxml.html.fromstring(tag_text)
        i_tag = root.find('.//i')
        return cls.parse_postal_code_and_city(i_tag.tail)

    @classmethod
    @catch_errors
    def parse_postal_code_and_city(cls, text: str):
        # example: ' 59602 Rüthen'
        if not text:
            return None, None
        split: list = text.strip().split(' ', 1)
        if len(split) != 2:
            cls.get_class_logger().debug(f'Could not split the postal code and city text into two parts. Got {len(split)}')
            return None, None

        postal_code = None
        match = re.search('\d{5}', text)
        if match:
            postal_code = match.group()
            text = text.replace(postal_code, '')

        # postal_code, city = split
        city = text.replace('\t', ' ').replace(u'\u200B', '').replace('\n', '').strip()
        city = re.sub(r'\s+', ' ', city).strip()
        return postal_code, city

    @classmethod
    def extract_and_parse_time(cls, text: str):
        t_set = set(re.findall(r'\d{2}:\d{2}', text))
        if len(t_set) > 1:
            cls.get_class_logger().warning(f'Found more than one time in {text=}: {t_str}')
        if len(t_set) == 0:
            cls.get_class_logger().warning(f'Found no time in {text=}')
            return None
        return datetime.time.fromisoformat(t_set.pop())

    @classmethod
    @catch_errors
    def parse_online_since(cls, text: str):
        # example ' Heute, 21:38'
        # '\n                                    \n                                        Heute, 07:59\n                                    \n                                        Heute, 07:59'
        text = text.strip()
        if not text:
            return None
        if "Heute" in text:
            d = datetime.date.today()
            t = cls.extract_and_parse_time(text)
            return datetime.datetime.combine(d, t)
        elif "Gestern" in text:
            d = datetime.datetime.now() - datetime.timedelta(1)
            t = cls.extract_and_parse_time(text)
            return datetime.datetime.combine(d, t)
        else:
            # TODO change- wrong format. is '05-08-2022', datetime expects YYYY-MM-DDTHH:MM:SS. mmmmmm
            return datetime.date.fromisoformat(text.replace(".", "-"))

    @classmethod
    @catch_errors
    def scalp_tags(cls, item, tags: List[str]):
        for tag in tags:
            if 'Zimmer' in tag:
                item['rooms'] = EbayKleinanzeigenSpider.parse_rooms(tag)
            if 'm²' in tag:
                item['area'] = EbayKleinanzeigenSpider.parse_area(tag)

    def parse(self, response, **kwargs):
        self.logger.info(f'Scalping {response.request.url}')

        page_str = response.text

        if response.text.count('<div') != response.text.count('</div'):
            logging.warning(f'Page {response.request.url} has a different number of <div> {response.text.count("<div")} and </div> {response.text.count("</div")} tags. Trying to fix it.')
            fixed_page = response.text
            fixed_page = fixed_page.replace('</article>', '</div></article> ')
            logging.debug(f'div count: {fixed_page.count("<div")} and </div> count: {fixed_page.count("</div")}')
            if fixed_page.count('<div') != fixed_page.count('</div'):
                logging.warning(f'Could not fix the page {response.request.url}')
            else:
                # response.body = fixed_page.encode('utf-8')
                response = response.replace(body=fixed_page.encode('utf-8'))

        css_index_selector = '.aditem'
        next_page_css_selector = '.pagination-next'
        elements = response.css(css_index_selector)
        if not elements:
            self.logger.warning(f'Maybe rate limited. Not elements found on the page: {response.request.url}')
        for elem in elements:
            source_id = elem.xpath("@data-adid").get()
            # self.logger.debug(f'processing item with source_id={source_id}')

            item = EbayKleinanzeigenItem()
            item.source_id = source_id
            # item.url = elem.xpath("@data-href").get()
            item.price = self.parse_price(elem.css('.aditem-main--middle--price-shipping--price::text').get())
            item.postal_code, item.city = self.parse_postal_code_and_city_from_div_tag(elem.css('.aditem-main--top--left').get())
            # item.postal_code, item.city = self.parse_postal_code_and_city(''.join(elem.css('.aditem-main--top--left::text').getall()))


            item.online_since = self.parse_online_since(''.join(elem.css('.aditem-main--top--right::text').getall()))
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
                next_page_url = f'{Config.BASE_URL}{href}'
                yield scrapy.Request(next_page_url, callback=self.parse, headers=self.get_headers())
            else:
                self.logger.debug(f'href not found in the next_page_selector')
