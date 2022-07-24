from src import persistence
from src.parsers.scrapy2db_parsers import EbayKleinanzeigenParser
from ...default_pipelines import DefaultPersistencePipeline


class EbayKleinanzeigenPersistencePipeline(DefaultPersistencePipeline):
    repository = persistence.EbayKleinanzeigenRepository
    parser = EbayKleinanzeigenParser
