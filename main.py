import configuration  # noinspection Do not delete
import logging
#from src.scrapers.ebay_kleinanzeigen.run import run_spider
#from src.scrapers.immonet.run import run_spider
#from src.scrapers.immowelt.run import run_spider


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    # run_spider()
    from src import persistence
    all = persistence.ImmoweltPostalCodeRepository.read_all_pageable(page=0, page_size=100)
    print(len(all))
    print(all[0], all[-1])

