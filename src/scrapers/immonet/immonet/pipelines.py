from src import persistence
from src.parsers.scrapy2db_parsers import ImmonetParser
from ...default_pipelines import DefaultPersistencePipeline


class ImmonetPersistencePipeline(DefaultPersistencePipeline):
    repository = persistence.ImmonetRepository
    parser = ImmonetParser
