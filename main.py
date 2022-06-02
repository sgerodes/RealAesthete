import configuration  # noinspection Do not delete
import logging
# from src.scraper.ebay_kleinanzeigen.run import run_spider
from src.scraper.immonet.run import run_spider

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    run_spider()
