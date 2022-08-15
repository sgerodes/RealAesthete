import datetime
import os


class ImmoweltSpiderConfig:
    BASE_URL = 'https://www.immowelt.de/'
    ENVIRONMENT_RANDOM_DECLINE_RATE = os.getenv('IMMOWELT_SPIDER_RANDOM_DECLINE_RATE')
    ABSOLUTE_TIMEDELTA_THRESHOLD = datetime.timedelta(days=7)
    MINIMUM_RANDOM_DECLINE_RATE = 0.1
    MAXIMUM_RANDOM_DECLINE_RATE = 0.5
    DEFAULT_RANDOM_DECLINE_RATE = 0.3
    RANDOM_DECLINE_RATE_PERIOD = datetime.timedelta(days=14)