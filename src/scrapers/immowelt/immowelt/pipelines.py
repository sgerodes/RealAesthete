from src import persistence
from src.parsers.scrapy2db_parsers import ImmoweltParser
from ...default_pipelines import DefaultPersistencePipeline
from .spiders.immowelt_base import ImmoweltSpider, ImmoweltItem


class ImmoweltPersistencePipeline(DefaultPersistencePipeline):
    DUPLICATES_THRESHOLD = 7
    repository = persistence.ImmoweltRepository
    parser = ImmoweltParser

    def on_too_many_duplicates(self, item: ImmoweltItem, spider: ImmoweltSpider):
        spider.stop_searching_on_postal_code(item.postal_code)
