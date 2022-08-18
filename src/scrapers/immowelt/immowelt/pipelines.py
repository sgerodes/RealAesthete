from src import persistence
from src.parsers.scrapy2db_parsers import ImmoweltParser
from ...default_pipelines import DefaultPersistencePipeline
from .spiders.immowelt_base import ImmoweltSpider, ImmoweltItem
from configuration.scrapy_configuration import ImmoweltScrapingConfig as Config


class ImmoweltPersistencePipeline(DefaultPersistencePipeline):
    DUPLICATES_THRESHOLD = Config.IMMOWELT_PERSISTENCE_PIPELINE_DUPLICATES_THRESHOLD
    repository = persistence.ImmoweltRepository
    parser = ImmoweltParser

    def on_too_many_duplicates(self, item: ImmoweltItem, spider: ImmoweltSpider):
        spider.logger.debug(f'Duplicate count on postal_code={item.postal_code} hit the threshold of {self.DUPLICATES_THRESHOLD}. Stopping the spider.')
        spider.stop_searching_on_postal_code(item.postal_code)
        self.duplicates_score = 0
