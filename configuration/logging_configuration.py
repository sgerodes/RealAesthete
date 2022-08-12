import datetime
import logging
import logging.config
import logging.handlers
import os

logger = logging.getLogger(__name__)
DEFAULT_LOG_LEVEL = 'DEBUG'
LOGS_FOLDER = '.logs'


def get_project_log_level():
    project_log_level = os.getenv('PROJECT_LOG_LEVEL', DEFAULT_LOG_LEVEL)
    available_log_levels = list(logging._nameToLevel.keys())
    if project_log_level not in available_log_levels:
        logging.warning(f'The specified logging level "{project_log_level}" is not recognised. Available levels are: {available_log_levels}')
        project_log_level = DEFAULT_LOG_LEVEL
    return project_log_level


def configure_logging():
    project_log_level = get_project_log_level()
    logging.warning(f'Project log level is set to {project_log_level}')

    logger_configuration_dict = {
        'version': 1,

        'formatters': {
            'default_fmt': {
                'format': '%(process)d | %(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'small_fmt': {
                'format': '[%(levelname)s] %(name)s: %(message)s'
            },
            'rate_stats_format': {
                'format': '%(asctime)s | %(message)s'
            },
            'error_email_fmt': {
                'format': '[%(levelname)s] %(name)s: %(message)s'
            },
        },

        'handlers': {
            'default': {
                'level': project_log_level,
                'formatter': 'small_fmt',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            }
        },

        'loggers': {
            '': {
                'handlers': ['default'],
                'level': project_log_level,
                'propagate': False
             },
            'scrapy': {
                'handlers': ['default'],
                'level': logging.DEBUG,
                'propagate': False
            },
            'sqlalchemy.engine.Engine': {
                'level': logging.WARNING,
                'propagate': True
            },
            'sqlalchemy.engine': {
                'level': logging.WARNING,
                'propagate': True
            },
            'urllib3.connectionpool': {
                'level': logging.WARNING,
            },
        }
    }
    if os.getenv('ENABLE_RATE_STATS_FILE_LOGGING', '').upper() == 'TRUE':
        logger.warning('Rate stats file logging is enabled')
        logger_config = {
                # file logger for creation and reading rate
                'level': logging.DEBUG,
                'handlers': ['rate_stats_file_handler'],
            }
        handler_config = {
                'level': 'DEBUG',
                'formatter': 'rate_stats_format',
                'class': 'logging.FileHandler',
                'filename': f'{LOGS_FOLDER}/rate_stats_{int(datetime.datetime.now().timestamp())}.log',
                'mode': 'a',
            }
        logger_configuration_dict['handlers']['rate_stats_file_handler'] = handler_config
        logger_configuration_dict['loggers']['src.scrapers.utils'] = logger_config

    logging.config.dictConfig(logger_configuration_dict)


