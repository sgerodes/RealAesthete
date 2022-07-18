import scrapy
import logging
from ..items import *
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



class ImmoweltSpider:
    BASE_URL = 'https://www.immowelt.de/'
    BASE_SEARCH_URL = 'https://www.immowelt.de/liste/muenchen-maxvorstadt/wohnungen/mieten?zip={zip_code}'
    # sorted by newest
    BASE_SEARCH_URL = 'https://www.immowelt.de/liste/{zip_code}/wohnungen/mieten?d=true&sd=DESC&sf=TIMESTAMP&sp=1'

    def get_url_for_zip_code(self, zip_code: int):
        # This will work for every zip code
        return ImmoweltSpider.BASE_SEARCH_URL.format(zip_code=str(zip_code))

    def start_requests(self):
        ua = UserAgent()
        headers = get_random_header_set()
        headers["User-Agent"] = ua.random
        yield scrapy.http.Request(self.start_urls[0], headers=headers)
