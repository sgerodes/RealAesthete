import sqlalchemy
import os
from . import models
from .repositories import *


engine = sqlalchemy.create_engine(os.getenv('DB_CONNECTION_STRING'), echo=False)
session = sqlalchemy.orm.sessionmaker(bind=engine)()

models.Base.metadata.create_all(engine)
