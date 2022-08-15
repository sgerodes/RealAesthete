import scrapy
from . import utils


class BaseSpider(scrapy.Spider):
    @utils.classproperty
    def name(cls):
        return cls.__name__
