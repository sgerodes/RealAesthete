from src import persistence
from src.parsers.scrapy2db_parsers import ImmoweltParser
from ...default_pipelines import DefaultPersistencePipeline


class ImmoweltPersistencePipeline(DefaultPersistencePipeline):
    DUPLICATES_THRESHOLD = 7
    repository = persistence.ImmoweltRepository
    parser = ImmoweltParser
