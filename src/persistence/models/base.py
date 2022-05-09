import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Numeric, DateTime, Enum as SqlalchemyEnum, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PythonEnum
import logging

logger = logging.getLogger(__name__)


engine = create_engine(os.getenv('DB_CONNECTION_STRING'), echo=True)
Base = declarative_base()


class EstateSource(PythonEnum):
    EbayKleinanzeigen = 'EbayKleinanzeigen'


class ExpositionType(PythonEnum):
    RENT = "RENT"
    SELL = "SELL"


class EstateType(PythonEnum):
    HOUSE = "HOUSE"
    FLAT = "FLAT"


class Estate:

    id = Column(Integer, primary_key=True)
    source = Column(SqlalchemyEnum)
    exposition_type = Column(SqlalchemyEnum)
    estate_type = Column(SqlalchemyEnum)

    price = Column(Numeric(precision=2))
    area = Column(Float)
    postal_code = Column(Integer)
    url = Column(String)

    db_entry_created = Column(DateTime(timezone=True), server_default=func.now())

    # TODO shift to child
    source_id = Column(String)
    title = Column(String)
    rooms = Column(Float)
    city = Column(String)
    build_year = Column(Integer)
    online_since = Column(DateTime(timezone=True))
    with_agent = Column(Boolean)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} price={self.price} area={self.area})'



