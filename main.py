import configuration
configuration.configure_project()  # noinspection Do not delete
import logging
from src.scrapers.ebay_kleinanzeigen import run as ebay_kleinanzeigen_run
from src.scrapers.immonet import run as immonet_run
from src.scrapers.immowelt import run as immowelt_run
from src.scrapers import utils
from src import persistence


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    e_count = persistence.EbayKleinanzeigenRepository.count()
    in_count = persistence.ImmonetRepository.count()
    iw_count = persistence.ImmoweltRepository.count()
    total_count = e_count + in_count + iw_count
    logger.info(f'DB has {e_count} EbayKleinanzeigen entries')
    logger.info(f'DB has {in_count} Immonet entries')
    logger.info(f'DB has {iw_count} Immowelt entries')
    logger.info(f'DB has a total of {total_count} entries ')

    spiders_and_settings = list()
    spiders_and_settings.extend(ebay_kleinanzeigen_run.get_spider_and_settings())
    spiders_and_settings.extend(immonet_run.get_spider_and_settings())
    spiders_and_settings.extend(immowelt_run.get_spider_and_settings())
    utils.run_parallel_spiders_2(spiders_and_settings)

    e_count_after = persistence.EbayKleinanzeigenRepository.count()
    in_count_after = persistence.ImmonetRepository.count()
    iw_count_after = persistence.ImmoweltRepository.count()
    total_count_after = e_count_after + in_count_after + iw_count_after
    logger.info(f'DB has {e_count_after} EbayKleinanzeigen entries. New {e_count_after - e_count}')
    logger.info(f'DB has {in_count_after} Immonet entries. New {in_count_after - in_count}')
    logger.info(f'DB has {iw_count_after} Immowelt entries. New {iw_count_after - iw_count}')
    logger.info(f'DB has a total of {total_count_after} entries. New {total_count_after - total_count}')
