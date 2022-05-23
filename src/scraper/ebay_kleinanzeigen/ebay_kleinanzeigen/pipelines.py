from .... import persistence
from ....persistence.models.ebay_kleinanzeigen import EbayKleinanzeigen
import logging


logger = logging.getLogger(__name__)

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EbayKleinanzeigenPersistencePipeline:
    DUPLICATES_THRESHOLD = 15
    duplicates = 0

    def __init__(self):
        self.name = self.__class__.__name__

    def process_item(self, item, spider):
        logger.debug(f'processing item with source_id={item.get("source_id")}')
        db_item = EbayKleinanzeigen(from_scrapy_item=item)
        db_entry = persistence.service.read_ebay_kleinanzeigen_by_source_id(item.get('source_id'))
        if db_entry:
            logger.debug(f'duplicate found. Duplicates {self.duplicates}')
            self.duplicates += 1
        else:
            persistence.service.save_estate_entity(db_item)
        if self.duplicates > self.DUPLICATES_THRESHOLD:
            logger.debug(f'Duplicate count hit the threshold of {self.DUPLICATES_THRESHOLD}. Stopping the spider')
            self.duplicates = 0
            spider.crawler.engine.close_spider(self, reason='to many duplicates')
        return item
