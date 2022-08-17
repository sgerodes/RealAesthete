import logging
from ..items import *
from fake_useragent import UserAgent
from src import persistence
from typing import List, Callable, Optional
import datetime
import random
from ..items import ImmoweltItem
from scrapy.exceptions import CloseSpider
from ....generic import BaseSpider
from configuration.scrapy_configuration import ImmoweltScrapingConfig as Config
from src.scrapers.utils import catch_errors


# logger = logging.getLogger(__name__)


class ImmoweltSpider(BaseSpider):
    ONE_DAY_TIMEDELTA = datetime.timedelta(days=1)
    RANDOM_DECLINE_RATE = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.postal_codes_to_stop_searching = set()
        self.set_random_decline_rate()

    def set_random_decline_rate(self):
        if Config.ENVIRONMENT_RANDOM_DECLINE_RATE:
            self.RANDOM_DECLINE_RATE = float(Config.ENVIRONMENT_RANDOM_DECLINE_RATE)
            self.logger.info(f'RANDOM_DECLINE_RATE is set by environment to {self.RANDOM_DECLINE_RATE}')
            return
        immowelt = persistence.ImmoweltRepository.read_first(estate_type=self.estate_type, exposition_type=self.exposition_type)
        if immowelt and immowelt.created_at:
            self.logger.debug(f'Time passed since first entry: {datetime.datetime.utcnow() - immowelt.created_at}. Calculation RANDOM_DECLINE_RATE from based on {immowelt}')
            timedelta_since_first_entry = datetime.datetime.utcnow() - immowelt.created_at
            if timedelta_since_first_entry > Config.RANDOM_DECLINE_RATE_PERIOD:
                self.RANDOM_DECLINE_RATE = Config.MINIMUM_RANDOM_DECLINE_RATE
                self.logger.info(f'More than {Config.RANDOM_DECLINE_RATE_PERIOD} passed since the first entry. '
                             f'RANDOM_DECLINE_RATE set to minimum = {self.RANDOM_DECLINE_RATE}')
                return
            else:
                ratio = timedelta_since_first_entry / Config.RANDOM_DECLINE_RATE_PERIOD
                decline_rate_span = Config.MAXIMUM_RANDOM_DECLINE_RATE - Config.MINIMUM_RANDOM_DECLINE_RATE
                self.RANDOM_DECLINE_RATE = Config.MINIMUM_RANDOM_DECLINE_RATE + decline_rate_span - (decline_rate_span * ratio)
                self.logger.info(f'calculated RANDOM_DECLINE_RATE: {self.RANDOM_DECLINE_RATE}')
                return

        if not self.RANDOM_DECLINE_RATE:
            self.RANDOM_DECLINE_RATE = Config.MAXIMUM_RANDOM_DECLINE_RATE
            self.logger.info(f'RANDOM_DECLINE_RATE is set to maximum = {self.RANDOM_DECLINE_RATE}')

    def stop_searching_on_postal_code(self, postal_code: str):
        self.postal_codes_to_stop_searching.add(postal_code)

    @classmethod
    @catch_errors
    def parse_source_id(cls, item_css_selector):
        return item_css_selector.css('a::attr(id)').get()

    @classmethod
    @catch_errors
    def parse_price(cls, item_css_selector) -> Optional[float]:
        text: str = item_css_selector.css('[data-test="price"]::text').get()
        if text == 'auf Anfrage':
            return None
        return float(text.replace('€', '').replace('.', '').replace(',', '.').strip())

    @classmethod
    @catch_errors
    def parse_area(cls, item_css_selector) -> Optional[float]:
        text: str = item_css_selector.css('[data-test="area"]::text').get()
        if not text:
            return None
        return float(text.replace('m²', '').strip())

    @classmethod
    @catch_errors
    def parse_rooms(cls, item_css_selector) -> Optional[float]:
        text: str = item_css_selector.css('[data-test="rooms"]::text').get()
        if not text:
            return None
        return float(text.replace('Zi.', '').strip())

    @classmethod
    @catch_errors
    def parse_city(cls, item_css_selector) -> str:
        text: str = item_css_selector.css("[class^='IconFact']").css('span::text').get()
        return text

    def start_requests(self):
        ua = UserAgent()
        all = persistence.ImmoweltPostalCodeStatisticsRepository.read_all(estate_type=self.estate_type,
                                                                          exposition_type=self.exposition_type)
        random.shuffle(all)
        all_postal_codes_filtered = list()
        for ipcs in all:
            should_search = False

            delta_since_last_search: datetime.timedelta = datetime.datetime.utcnow() - ipcs.last_search if ipcs.last_search else None
            if not delta_since_last_search or delta_since_last_search > Config.ABSOLUTE_TIMEDELTA_THRESHOLD:
                if random.random() > self.RANDOM_DECLINE_RATE:
                    # self.logger.debug('Will crawl, too much time passed since last search')
                    should_search = True
                else:
                    # self.logger.debug('Will not crawl, because of the random decline rule')
                    continue

            delta_since_created: datetime.timedelta = datetime.datetime.utcnow() - ipcs.created_at
            frequency: datetime.timedelta = delta_since_created / ipcs.total_entries if ipcs.total_entries != 0 else datetime.timedelta(weeks=10000)
            # if not should_search and frequency < self.ONE_DAY_TIMEDELTA:
            #     self.logger.debug('Will crawl, because of frequency very high')
            #     should_search = True

            if not should_search and delta_since_last_search > frequency:
                # self.logger.debug('Will crawl, because of frequency')
                should_search = True

            if should_search:
                all_postal_codes_filtered.append(ipcs)

        self.logger.info(f'Based on filters will search {len(all_postal_codes_filtered)} postal codes')

        for ipcs in all_postal_codes_filtered:
            headers = {} # get_random_header_set()
            headers["User-Agent"] = ua.random
            url = self.start_urls[0].format(postal_code=ipcs.postal_code, page=1)
            yield scrapy.http.Request(url, headers=headers, cb_kwargs={'postal_code': ipcs.postal_code, 'page': 1})

    def parse(self, response, postal_code: str, page: int):  # noqa
        self.logger.debug(f'parsing url {response.request.url}')

        css_index_selector = "[class^='EstateItem']"

        if response.status == 404:
            self.logger.warning(f'Request for postal_code={postal_code} is 404. response.request.url={response.request.url}')

        elements_selector = response.css(css_index_selector)

        if response.css('body'):
            # This means we got blocked
            ipcs = persistence.ImmoweltPostalCodeStatisticsRepository.read_by_unique(estate_type=self.estate_type,
                                                                                     exposition_type=self.exposition_type,
                                                                                     postal_code=postal_code)
            ipcs.last_search = datetime.datetime.utcnow()
            persistence.ImmoweltPostalCodeStatisticsRepository.update(ipcs)
        else:
            self.logger.error(f'No body tag. We are probably blocked. response.body={response.body}')
            # spider.crawler.engine.close_spider(self, reason=f'to many duplicates {spider.name}')
            raise CloseSpider('No body tag. We are probably blocked.')

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
            if postal_code not in self.postal_codes_to_stop_searching:
                new_page = page + 1
                next_page_url = self.start_urls[0].format(postal_code=postal_code, page=new_page)
                self.logger.debug(f'going to the next page {next_page_url}')
                yield scrapy.Request(next_page_url, callback=self.parse, cb_kwargs={'postal_code': postal_code, 'page': new_page})
            else:
                self.logger.debug(f'Stopping searching on {postal_code=}')

        else:
            self.logger.debug('No elements found on the page')
