from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from typing import List, Tuple, Callable
import scrapy
import datetime
import logging
import inspect
from . import generic
from configuration.scrapy_configuration import SharedSpiderConfig


logger = logging.getLogger(__name__)


def run_parallel_spiders(spiders, project_settings):
    for s in spiders:
        runner = CrawlerRunner(settings=project_settings)
        runner.crawl(s)

    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()


def run_parallel_spiders_2(spiders_and_settings: List[Tuple[scrapy.spiders.Spider, str]]):
    activate_spiders = SharedSpiderConfig.ACTIVE_SPIDERS
    if not activate_spiders:
        logger.warning('ACTIVATE_SPIDERS env variable is not set. Will not crawl')
        return

    activate_spiders_set = set(name.strip() for name in activate_spiders.split(','))
    logger.debug(f'Will activate spiders: {activate_spiders}')
    spiders_to_activate = list()
    for s in spiders_and_settings:
        spider = s[0]
        if activate_spiders.upper() == 'ALL' or spider.name in activate_spiders_set:
            logger.debug(f'Will activate spider {spider.name}')
            spiders_to_activate.append(s)
        else:
            logger.debug(f'Will NOT activate spider {spider.name}')

    for s in spiders_to_activate:
        spider = s[0]
        settings = s[1]
        runner = CrawlerRunner(settings=settings)
        runner.crawl(spider)

    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()


class PersistencePipelineStatsService:
    def __init__(self, name: str):
        self.name = name
        self.first_create = datetime.datetime.utcnow()
        self.total_read = 0
        self.total_created = 0

    def add_read(self):
        self.total_read += 1
        rate = (datetime.datetime.utcnow() - self.first_create) / self.total_read
        # logger.debug(f'{self.name} reading rate is {rate}')
        #entity = persistence.PersistencePipelineStats()
        #entity.name = self.name
        #entity.set_type_reading()
        #entity.set_rate_from_timedelta(rate)
        #persistence.PersistencePipelineStatsRepository.create(entity)

    def add_create(self):
        self.total_created += 1
        rate = (datetime.datetime.utcnow() - self.first_create) / self.total_created
        # logger.debug(f'{self.name} creation rate is {rate}')
        #entity = persistence.PersistencePipelineStats()
        #entity.name = self.name
        #entity.set_type_creation()
        #entity.set_rate_from_timedelta(rate)
        #persistence.PersistencePipelineStatsRepository.create(entity)

class cached_classproperty:  # noqa
    """
    https://github.com/hottwaj/classproperties/blob/main/classproperties
    """
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        val = self.fget(owner_cls)
        setattr(owner_cls, self.fget.__name__, val)
        return val


class classproperty:
    """
    https://github.com/hottwaj/classproperties/blob/main/classproperties
    Decorator for a Class-level property.  Credit to Denis Rhyzhkov on Stackoverflow: https://stackoverflow.com/a/13624858/1280629
    """
    def __init__(self, fget, cached=False):
        self.fget = fget
        self.cached=cached

    def __get__(self, owner_self, owner_cls):
        val = self.fget(owner_cls)
        if self.cached:
            setattr(owner_cls, self.fget.__name__, val)
        return val


# should only be used for scrapy spiders
def catch_errors(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log = logger
            args_without_self = args
            if args:
                self_or_cls = args[0]
                args_without_self = args[1:]
                if inspect.isclass(self_or_cls) and issubclass(self_or_cls, generic.BaseSpider):
                    log = self_or_cls.get_class_logger()
                elif isinstance(self_or_cls, scrapy.Spider):
                    if hasattr(self_or_cls, 'logger'):
                        log = self_or_cls.logger
                    else:
                        log.warning('Spider instance has no attribute "logger"')
                else:
                    log.warning('Class of bound method is not of instance or type scrapy.Spider')
            log.warning(f'Error occurred while executing function "{func.__name__}" with args={args_without_self}, kwargs={kwargs}')
            log.exception(e)
            return None
    return wrapper
