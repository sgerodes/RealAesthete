import sqlalchemy
import os
from . import models
from .repositories import *
from . import utils


sqlalchemy_database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
if sqlalchemy_database_uri.startswith('postgresql'):
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'), echo=False, pool_size=40, max_overflow=0)
else:
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'), echo=False)

models.Base.metadata.create_all(engine)

Repository.set_engine(engine)
