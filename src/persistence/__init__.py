import sqlalchemy
import os
from . import models
from .repositories import *
from . import utils


sqlalchemy_database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
if sqlalchemy_database_uri.startswith('postgresql'):
    pool_size = int(os.getenv('POSTGRES_POOL_SIZE', 40))
    max_overflow = int(os.getenv('POSTGRES_MAX_OVERFLOW', 10))
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'),
                                      echo=False,
                                      pool_size=pool_size,
                                      max_overflow=max_overflow)
else:
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'), echo=False)

models.Base.metadata.create_all(engine)

Repository.set_engine(engine)
