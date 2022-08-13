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
    # spiders_and_settings = list()
    # spiders_and_settings.extend(ebay_kleinanzeigen_run.get_spider_and_settings())
    # spiders_and_settings.extend(immonet_run.get_spider_and_settings())
    # spiders_and_settings.extend(immowelt_run.get_spider_and_settings())
    # utils.run_parallel_spiders_2(spiders_and_settings)
    print(len(persistence.ImmoweltPostalCodeStatisticsRepository.read_all(exposition_type="RENT", estate_type="FLAT", last_search=None)))
    print(len(persistence.ImmoweltPostalCodeStatisticsRepository.read_all(persistence.ImmoweltPostalCodeStatistics.last_search != None,
                                                                          persistence.ImmoweltPostalCodeStatistics.total_entries != 0,
                                                                          exposition_type="RENT",
                                                                          estate_type="FLAT")))
    print(len(persistence.ImmoweltPostalCodeStatisticsRepository.read_all(persistence.ImmoweltPostalCodeStatistics.last_search != None,
                                                                          persistence.ImmoweltPostalCodeStatistics.total_entries == 0,
                                                                          exposition_type="RENT",
                                                                          estate_type="FLAT")))
