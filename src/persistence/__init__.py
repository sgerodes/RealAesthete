import logging
import sqlalchemy
import os
from . import models
from .repositories import *
from . import utils
from configuration.sqlalchemy_configuration import PostgresConfiguration, SqlalchemyConfiguration


logger = logging.getLogger(__name__)


if SqlalchemyConfiguration.DATABASE_URI.startswith('postgresql'):
    pool_size = PostgresConfiguration.POOL_SIZE
    max_overflow = PostgresConfiguration.MAX_OVERFLOW
    logger.info(f'Setting postgres engine settings to {pool_size=}, {max_overflow=}')
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'),
                                      echo=False,
                                      pool_size=pool_size,
                                      max_overflow=max_overflow)
else:
    engine = sqlalchemy.create_engine(SqlalchemyConfiguration.DATABASE_URI, echo=False)

models.Base.metadata.create_all(engine)

Repository.set_engine(engine)
