import scrapy
import logging
from ..items import ImmonetItem
from ....headers import get_random_header_set
from fake_useragent import UserAgent
import re
import datetime
from src import persistence
from typing import List, Callable, Optional
from ....generic import BaseSpider
from configuration.scrapy_configuration import ImmonetScrapingConfig as Config
from src.scrapers.utils import catch_errors


# logger = logging.getLogger(__name__)


class ImmonetSpider(BaseSpider):
    def start_requests(self):
        yield scrapy.http.Request(self.start_urls[0], headers=self.get_headers())

    @classmethod
    @catch_errors
    def parse_price(cls, text: str):
        # example: '1.040 '
        if not text:
            return
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found.replace('.', '').replace(',', '.').replace('€', '')
        return None

    @classmethod
    @catch_errors
    def parse_city(cls, text: str):
        # example: 'Etagenwohnung • Coswig '
        if not text:
            return
        city = text.split('•')[1].strip()\
            .replace('\n', '')\
            .replace('\r', '')\
            .replace('\t\t\t\t\t\t\t', ' ')
        split = city.split(' ')
        if len(split) == 2 and split[0] == split[1]:
            city = split[0]
        return city

    @classmethod
    @catch_errors
    def parse_rooms(cls, text: str) -> Optional[float]:
        if text is None:
            return None
        # example: ' 3.5 '
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found
        return None

    @classmethod
    @catch_errors
    def parse_area(cls, text: str) -> Optional[float]:
        # example: ' 44 '
        if not text:
            return None
        search = re.compile(r'[\d\.]+').search(text)
        if search:
            found = search.group(0)
            return found
        return None

    @classmethod
    @catch_errors
    def parse_item_id(cls, text):
        if not text:
            return
        return text.split('_')[1]

    def parse(self, response, **kwargs):
        self.logger.info(f'Scalping url {response.request.url}')
        css_index_selector = '.item'
        next_page_css_selector = '.text-right'

        for elem in response.css(css_index_selector):
            source_id = self.parse_item_id(elem.xpath("@id").get())
            self.logger.debug(f'parsing item with source_id={source_id}')

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
            if source_id:
                yield scrapy.Request(f'https://www.immonet.de/angebot/{source_id}',
                                     callback=self.parse_detailed_page,
                                     cb_kwargs={'source_id': source_id},
                                     headers=self.get_headers())
            else:
                self.logger.warning(f'No source_id found for element')

        next_page_selector = response.css(next_page_css_selector)
        if next_page_selector:
            href = next_page_selector.xpath('@href').get()
            if href:
                next_page_url = f'{Config.BASE_URL}{href}'
                self.logger.debug(f'Spider {self.__class__.__name__}: going to the next page {next_page_url}')
                yield scrapy.Request(next_page_url, callback=self.parse, headers=self.get_headers())
            else:
                self.logger.debug(f'Spider  {self.__class__.__name__}: href not found in the next_page_selector')

    def parse_detailed_page(self, response, source_id: str, **kwargs):
        self.logger.debug(f'Scraping detailed {source_id=}')
        immonet = persistence.ImmonetRepository.read_by_source_id(source_id)
        if not immonet:
            self.logger.error(f'Scrapy detailed page for {source_id=}, but no corresponding db model was found')
            return None

        postal_code = ImmonetPostalCodeSpider.parse_postal_code(response.css('.show').css('.text-100.pull-left').get(), source_id)
        if postal_code:
            immonet.postal_code = postal_code
            persistence.ImmonetRepository.update(immonet)


class AbstractImmonetForeclosureSpider(ImmonetSpider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.piped = 0
        self.updated = 0

    def parse(self, *args, **kwargs):
        duplicates = 0
        for super_response in super().parse(*args, **kwargs):
            if isinstance(super_response, ImmonetItem) and super_response.source_id:
                db_entity = persistence.ImmonetRepository.read_by_source_id(super_response.source_id)
                if db_entity:
                    if db_entity.foreclosure is None:
                        db_entity.foreclosure = super_response.foreclosure
                        persistence.ImmonetRepository.update(db_entity)
                        self.updated += 1

                    else:
                        duplicates += 1
                        if duplicates >= Config.FORECLOSURE_SPIDER_DUPLICATES_THRESHOLD:
                            self.crawler.engine.close_spider(self, reason=f'to many duplicates {self.name}')
                    continue
            self.piped += 1
            yield super_response

    def closed(self, reason):
        self.logger.info(f'Updated {self.updated} entries')
        self.logger.info(f'Piped further {self.piped} entries')
        super().closed(reason)


class ImmonetPostalCodeSpider(BaseSpider):
    def __init__(self):
        self.updated_postal_codes = 0

    @classmethod
    @catch_errors
    def parse_postal_code(cls, text_with_html: str, source_id: str) -> Optional[str]:
        # example: ' 63636&nbsp; Brachttal '
        if not text_with_html:
            return None
        findall = re.compile(r'\d{5}').findall(text_with_html)
        if not findall:
            return None
        if len(findall) > 1:
            first = findall[0]
            for candidate in findall:
                if candidate != first:
                    cls.get_class_logger().warning(f'Found more than one postal code candidates for {source_id=}: {text_with_html}')
                    return None
        return findall[0]

    def start_requests(self):
        all = persistence.ImmonetRepository.read_all(persistence.Immonet.created_at > datetime.datetime.now() - datetime.timedelta(days=1), postal_code=None)
        self.logger.info(f'{len(all)} immonet entries have no postal_code')
        for immonet in all:
            url = f'https://www.immonet.de/angebot/{immonet.source_id}'
            yield scrapy.http.Request(url, headers=self.get_headers(), cb_kwargs={'source_id': immonet.source_id, 'immonet_model': immonet})

    def closed(self, reason):
        self.logger.info(f'Updated {self.updated_postal_codes} postal codes')
        super().closed(reason)

    def parse(self, response, immonet_model: persistence.Immonet, **kwargs):
        self.logger.debug(f'Scraping detailed {immonet_model.source_id=}')
        postal_code = self.parse_postal_code(response.css('.show').css('.text-100.pull-left').get(), immonet_model.source_id)
        if not postal_code:
            self.logger.warning(f'Could not find the postal code for {immonet_model}')
        else:
            # logger.debug(f'updating postal code to {postal_code}')
            immonet_model.postal_code = postal_code
            persistence.ImmonetRepository.update(immonet_model)
            self.updated_postal_codes += 1

