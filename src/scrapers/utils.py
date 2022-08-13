from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from typing import List, Tuple
import scrapy
import datetime
import logging
import os
from .. import persistence


logger = logging.getLogger(__name__)


def run_parallel_spiders(spiders, project_settings):
    for s in spiders:
        runner = CrawlerRunner(settings=project_settings)
        runner.crawl(s)

    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()


def run_parallel_spiders_2(spiders_and_settings: List[Tuple[scrapy.spiders.Spider, str]]):
    activate_spiders = os.getenv('ACTIVATE_SPIDERS')
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
        logger.debug(f'{self.name} reading rate is {rate}')
        entity = persistence.PersistencePipelineStats()
        entity.name = self.name
        entity.set_type_reading()
        entity.set_rate_from_timedelta(rate)
        persistence.PersistencePipelineStatsRepository.create(entity)

    def add_create(self):
        self.total_created += 1
        rate = (datetime.datetime.utcnow() - self.first_create) / self.total_created
        logger.debug(f'{self.name} creation rate is {rate}')
        entity = persistence.PersistencePipelineStats()
        entity.name = self.name
        entity.set_type_creation()
        entity.set_rate_from_timedelta(rate)
        persistence.PersistencePipelineStatsRepository.create(entity)

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