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



class ImmonetSpider:
    BASE_URL = 'https://www.immowelt.de/'
    # BASE_SEARCH_URL = 'https://www.immowelt.de/liste/muenchen-maxvorstadt/wohnungen/mieten?geoid=10809162000020%2C10809162000021%2C10809162000028&sort=relevanz&zip={zip_code}'
    BASE_SEARCH_URL = 'https://www.immowelt.de/liste/muenchen-maxvorstadt/wohnungen/mieten?zip={zip_code}'
    # sorted by newest
    BASE_SEARCH_URL = 'https://www.immowelt.de/liste/{zip_code}/wohnungen/mieten?d=true&sd=DESC&sf=TIMESTAMP&sp=1'

    def get_url_for_zip_code(self, zip_code: int):
        # This will work for every zip code
        return ImmonetSpider.BASE_SEARCH_URL.format(zip_code=str(zip_code))
