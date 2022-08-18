import logging
from . import utils
from configuration.scrapy_configuration import SharedSpiderConfig as Config

logger = logging.getLogger(__name__)


global_stats = utils.PersistencePipelineStatsService('Global')


class DefaultPersistencePipeline:
    DUPLICATES_THRESHOLD = Config.DEFAULT_PERSISTENCE_PIPELINE_DUPLICATES_THRESHOLD
    class_stats = None

    def __init__(self):
        self.name = self.__class__.__name__
        self.duplicates_score = 0.0
        if not hasattr(self, 'repository'):
            logger.error(f'You forgot to specify the repository for {self.__class__}')
        if not hasattr(self, 'parser'):
            logger.error(f'You forgot to specify the parser for {self.__class__}')

        self.__class__.class_stats = utils.PersistencePipelineStatsService(f'{self.__class__.__name__}')
        self.instance_stats = utils.PersistencePipelineStatsService(None)

    def process_item(self, item, spider):
        if not self.instance_stats.name:
            self.instance_stats.name = f'{spider.name}'

        global_stats.add_read()
        self.__class__.class_stats.add_read()
        self.instance_stats.add_read()

        db_model = self.repository.read_by_source_id(item.get('source_id'))
        if db_model:
            self.duplicates_score += 1
            spider.logger.debug(f'Duplicate found duplicates_score={self.duplicates_score}')
        else:
            new_db_model = self.parser.create_from_scrapy_item(item)
            self.repository.create(new_db_model)
            self.duplicates_score -= 0.5
            self.duplicates_score = max(self.duplicates_score, 0)

            global_stats.add_create()
            self.__class__.class_stats.add_create()
            self.instance_stats.add_create()

        if self.DUPLICATES_THRESHOLD is not None and self.duplicates_score > self.DUPLICATES_THRESHOLD:
            self.on_too_many_duplicates(item, spider)
        return item

    def on_too_many_duplicates(self, item, spider):
        spider.logger.info(f'Duplicate count hit the threshold of {self.DUPLICATES_THRESHOLD}. Stopping the spider.')
        spider.crawler.engine.close_spider(self, reason=f'{spider.name}: to many duplicates')
