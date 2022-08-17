import scrapy
from . import utils
from scrapy import signals
from pydispatch import dispatcher
import logging


class BaseSpider(scrapy.Spider):
    @utils.classproperty
    def name(cls):
        return cls.__name__

    def __init__(self, *args, **kwargs):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        super().__init__(*args, **kwargs)

    def spider_closed(self):
        self.logger.info(f'Spider closed')

    @classmethod
    def get_class_logger(cls):
        return logging.LoggerAdapter(logging.getLogger(cls.name), {'class': cls})