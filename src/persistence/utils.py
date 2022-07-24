import logging
import uuid
import sqlalchemy # noqa
import functools
from typing import Callable, TypeVar
from src import persistence, scrapers


logger = logging.getLogger(__name__)


VAR_REPOSITORY = TypeVar('VAR_REPOSITORY', bound='Repository')


def rollback_on_error(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlalchemy.exc.IntegrityError as e:
            logger.exception(e)
            logger.warning(f'Rolling back the db session because of the error')
            persistence.session.rollback()
            return None
        except sqlalchemy.exc.ProgrammingError as e:
            logger.exception(e)
            logger.warning(f'Rolling back the db session because of the error')
            persistence.session.rollback()
        except sqlalchemy.exc.DatabaseError as e:
            logger.exception(e)
            persistence.session.rollback()
            logger.warning('session rollbacked')
        except sqlalchemy.exc.InvalidRequestError as e:
            logger.exception(e)
            persistence.session.rollback()
            logger.warning('session rollbacked')
            return None
    return wrapper


def non_deletable(clazz: VAR_REPOSITORY) -> VAR_REPOSITORY:
    @classmethod # noqa
    def delete(cls, *args, **kwargs):
        logger.warning(f'It is not allowed to delete a "{cls._get_model_type_name()}"')
    setattr(clazz, 'delete', delete)
    return clazz


def non_updatable(clazz: VAR_REPOSITORY) -> VAR_REPOSITORY:
    @classmethod # noqa
    def update(cls, *args, **kwargs):
        logger.warning(f'It is not allowed to update a "{cls._get_model_type_name()}"')
    setattr(clazz, 'update', update)
    return clazz


def non_creatable(clazz: VAR_REPOSITORY) -> VAR_REPOSITORY:
    @classmethod # noqa
    def create(cls, *args, **kwargs):
        logger.warning(f'It is not allowed to create a "{cls._get_model_type_name()}"')
    setattr(clazz, 'create', create)
    return clazz


def persist(est, ext, pc_list):
    for postal_code in pc_list:
        persistence.ImmoweltPostalCodeStatisticsRepository.create_by_unique(postal_code=postal_code, estate_type=est,
                                                                            exposition_type=ext)
def init_immowelt_postal_code_statistics_repository():
    if not persistence.ImmoweltPostalCodeStatisticsRepository.read_by_primary_keys(1):
        logger.debug('Initialising ImmoweltPostalCodeStatistics table')
        with open('./resources/zip_code/immowelt/immowelt_postal_codes.csv', 'r') as f:
            postal_code_list = f.readlines()
            # #from multiprocessing import Pool, Process
            # from threading import Thread
            #
            # threads = list()
            # for estate_type in scrapers.enums.EstateType:
            #     for exposition_type in scrapers.enums.ExpositionType:
            #         threads.append(Thread(target=persist, args=(estate_type, exposition_type, postal_code_list)))
            #
            # for p in threads:
            #     p.start()
            #
            # for p in threads:
            #     p.join()

            # for estate_type in scrapers.enums.EstateType:
            #     for exposition_type in scrapers.enums.ExpositionType:
            #         for postal_code in postal_code_list:
            #             persistence.ImmoweltPostalCodeStatisticsRepository.create_by_unique(postal_code=postal_code, estate_type=estate_type, exposition_type=exposition_type)
    else:
        logger.debug('ImmoweltPostalCodeStatistics table is already initialised')
