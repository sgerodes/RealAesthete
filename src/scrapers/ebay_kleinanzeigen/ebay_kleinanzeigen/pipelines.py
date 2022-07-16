import logging
from src import persistence
from src.parsers.scrapy2db_parsers import EbayKleinanzeigenParser


logger = logging.getLogger(__name__)


class EbayKleinanzeigenPersistencePipeline:
    DUPLICATES_THRESHOLD = 15
    duplicates = 0

    def __init__(self):
        self.name = self.__class__.__name__

    def process_item(self, item, spider):
        logger.debug(f'processing item with source_id={item.get("source_id")}')
        db_model = persistence.EbayKleinanzeigenRepository.read_by_source_id(item.get('source_id'))
        if db_model:
            logger.debug(f'duplicate found. Duplicates {self.duplicates}')
            self.duplicates += 1
        else:
            new_db_model = EbayKleinanzeigenParser.create_from_scrapy_item(item)
            persistence.EbayKleinanzeigenRepository.create(new_db_model)
        if self.duplicates > self.DUPLICATES_THRESHOLD:
            logger.debug(f'Duplicate count hit the threshold of {self.DUPLICATES_THRESHOLD}. Stopping the spider')
            self.duplicates = 0
            spider.crawler.engine.close_spider(self, reason='to many duplicates')
        return item
