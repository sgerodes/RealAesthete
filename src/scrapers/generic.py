import scrapy
from . import utils
import logging
from .headers import get_random_header_set
from fake_useragent import UserAgent


class BaseSpider(scrapy.Spider):
    OPEN_SPIDERS = list()

    @utils.classproperty
    def name(cls):
        return cls.__name__

    def __init__(self, *args, **kwargs):
        BaseSpider.OPEN_SPIDERS.append(self.name)
        self.logger.info(f'Starting spider spiders: {self.name}. Open spiders: {BaseSpider.OPEN_SPIDERS}')
        super().__init__(*args, **kwargs)

    def closed(self, reason):
        if self.name in BaseSpider.OPEN_SPIDERS:
            BaseSpider.OPEN_SPIDERS.remove(self.name)
        else:
            self.logger.warning(f'Tried to remove a non existing name from the open spiders list OPEN_SPIDERS={BaseSpider.OPEN_SPIDERS}')
        self.logger.info(f'Spider closed. Open spiders: {BaseSpider.OPEN_SPIDERS}')

    def get_headers(self):
        headers = get_random_header_set()
        headers["User-Agent"] = self.get_random_usr_agent()
        return headers

    def get_random_usr_agent(self):
        ua = UserAgent()
        return ua.random

    @classmethod
    def get_class_logger(cls):
        return logging.LoggerAdapter(logging.getLogger(cls.name), {'class': cls})
