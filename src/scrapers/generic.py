import scrapy
from . import utils
from scrapy import signals
from pydispatch import dispatcher
import logging
from .headers import get_random_header_set
from fake_useragent import UserAgent


class BaseSpider(scrapy.Spider):
    @utils.classproperty
    def name(cls):
        return cls.__name__

    def __init__(self, *args, **kwargs):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        super().__init__(*args, **kwargs)

    def spider_closed(self):
        if hasattr(self, 'on_close'):
            self.on_close()
        self.logger.info(f'Spider closed')


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
