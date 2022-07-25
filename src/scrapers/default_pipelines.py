import logging
import datetime


logger = logging.getLogger(__name__)

first_create = datetime.datetime.utcnow()
total_read = 0
total_created = 0

class DefaultPersistencePipeline:
    DUPLICATES_THRESHOLD = 15

    def __init__(self):
        self.name = self.__class__.__name__
        self.duplicates_score = 0.0
        if not hasattr(self, 'repository'):
            logger.error(f'You forgot to specify the repository for {self.__class__}')
        if not hasattr(self, 'parser'):
            logger.error(f'You forgot to specify the parser for {self.__class__}')

    def process_item(self, item, spider):
        estate_type = spider.estate_type if hasattr(spider, 'estate_type') else ''
        exposition_type = spider.exposition_type if hasattr(spider, 'exposition_type') else ''

        global first_create
        global total_read
        global total_created

        total_read += 1
        logger.debug(f'Reading rate is {(datetime.datetime.utcnow() - first_create) / total_read}')

        logger.debug(f'processing item with source_id={item.get("source_id")}')
        db_model = self.repository.read_by_source_id(item.get('source_id'))
        if db_model:
            self.duplicates_score += 1
            logger.debug(f'Duplicate found {self.duplicates_score=}, {estate_type}, {exposition_type}')
        else:
            new_db_model = self.parser.create_from_scrapy_item(item)
            self.repository.create(new_db_model)
            self.duplicates_score -= 0.5
            self.duplicates_score = max(self.duplicates_score, 0)

            total_created += 1
            logger.debug(f'Creation rate is {(datetime.datetime.utcnow() - first_create) / total_created}')

        if self.duplicates_score > self.DUPLICATES_THRESHOLD:
            logger.debug(
                f'Duplicate count hit the threshold of {self.DUPLICATES_THRESHOLD}. Stopping the spider. {estate_type}, {exposition_type}')
            spider.crawler.engine.close_spider(self, reason='to many duplicates')
        return item