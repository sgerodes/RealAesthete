import scrapy
import logging
from ..items import *
from ....headers import get_random_header_set
from fake_useragent import UserAgent
from src import persistence
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

    def get_all_postal_code(self) -> List[str]:
        plz_10000_to_99999 = [str(plz) for plz in range(10 ** 4, 10 ** 5)]
        plz_to_10000 = [('00000' + str(plz))[-5:] for plz in range(10 ** 4)]
        return plz_to_10000 + plz_10000_to_99999

    def get_url_for_zip_code(self, zip_code: int):
        # This will work for every zip code
        return ImmoweltSpider.BASE_SEARCH_URL.format(zip_code=str(zip_code))

    def start_requests(self):
        ua = UserAgent()
        headers = get_random_header_set()
        headers["User-Agent"] = ua.random
        for iw_postal_code in persistence.ImmoweltPostalCodeRepository.read_all(exists=True):
            url = self.start_urls[0].format(postal_code=iw_postal_code.postal_code)
            yield scrapy.http.Request(url, headers=headers, cb_kwargs={'postal_code': iw_postal_code.postal_code})

    def parse(self, response, postal_code):
        logger.debug(f'Spider {self.__class__.__name__}: parsing url {response.request.url}')

        if response.status == 404:
            logger.warning(f'Request for {postal_code=} is 404. {response.request.url=}')
