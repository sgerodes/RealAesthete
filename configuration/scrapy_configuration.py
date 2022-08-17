import datetime
import os


class SharedSpiderConfig:
    DEFAULT_PERSISTENCE_PIPELINE_DUPLICATES_THRESHOLD = 15


class EbayKleinanzeigenScrapingConfig:
    BASE_URL = 'https://www.ebay-kleinanzeigen.de'


class ImmonetScrapingConfig:
    BASE_URL = 'https://www.immonet.de/'


class ImmoweltScrapingConfig:
    BASE_URL = 'https://www.immowelt.de/'
    ENVIRONMENT_RANDOM_DECLINE_RATE = os.getenv('IMMOWELT_SPIDER_RANDOM_DECLINE_RATE')
    ABSOLUTE_TIMEDELTA_THRESHOLD = datetime.timedelta(days=7)
    MINIMUM_RANDOM_DECLINE_RATE = 0.1
    MAXIMUM_RANDOM_DECLINE_RATE = 0.5
    DEFAULT_RANDOM_DECLINE_RATE = 0.3
    RANDOM_DECLINE_RATE_PERIOD = datetime.timedelta(days=14)
    FORECLOSURE_SPIDER_DUPLICATES_THRESHOLD = 15
    IMMOWELT_PERSISTENCE_PIPELINE_DUPLICATES_THRESHOLD = 7


