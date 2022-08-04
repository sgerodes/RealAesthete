import sqlalchemy
import os
from . import models
from .repositories import *
from . import utils


engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'), echo=False)
models.Base.metadata.create_all(engine)

Repository.set_engine(engine)
