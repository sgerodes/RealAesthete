from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import datetime
import logging
import os


logger = logging.getLogger(__name__)


def run_parallel_spiders(spiders, project_settings):
    for s in spiders:
        runner = CrawlerRunner(settings=project_settings)
        runner.crawl(s)

    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()


def run_parallel_spiders_2(spiders_and_settings):
    activate_spiders = os.getenv('ACTIVATE_SPIDERS')
    if not activate_spiders:
        logger.warning('ACTIVATE_SPIDERS env variable is not set. Will not crawl')
        return

    activate_spiders_set = set(activate_spiders.split(','))
    logger.debug(f'Will activate spiders {activate_spiders}')
    for s in spiders_and_settings:
        spider = s[0]
        settings = s[1]
        if activate_spiders.upper() == 'ALL' or spider.name in activate_spiders_set:
            logger.debug(f'Activating spider {spider.name}')
            runner = CrawlerRunner(settings=settings)
            runner.crawl(spider)
        else:
            logger.debug(f'Will not activate spider {spider.name}')

    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()


class PersistencePipelineStats:
    def __init__(self, name: str):
        self.name = name
        self.first_create = datetime.datetime.utcnow()
        self.total_read = 0
        self.total_created = 0

    def add_read(self):
        self.total_read += 1
        logger.debug(f'{self.name} reading rate is {(datetime.datetime.utcnow() - self.first_create) / self.total_read}')

    def add_create(self):
        self.total_created += 1
        logger.debug(f'{self.name} creation rate is {(datetime.datetime.utcnow() - self.first_create) / self.total_created}')
