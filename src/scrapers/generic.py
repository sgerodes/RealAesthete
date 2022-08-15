import scrapy
from . import utils
from scrapy import signals
from pydispatch import dispatcher


class BaseSpider(scrapy.Spider):
    @utils.classproperty
    def name(cls):
        return cls.__name__

    def __init__(self, *args, **kwargs):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        super().__init__(*args, **kwargs)

    def spider_closed(self):
        self.logger.info(f'Spider closed')
