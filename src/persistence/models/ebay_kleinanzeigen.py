from .base import Estate, Base, EstateSource
from sqlalchemy import create_engine, Column, Integer, String, Float, Numeric, DateTime, Enum as SqlalchemyEnum, Boolean, func


class EbayKleinanzeigen(Base, Estate):
    __tablename__ = 'EbayKleinanzeigen'

    # TODO shift to child
    source_id = Column(String)
    title = Column(String)
    rooms = Column(Float)
    city = Column(String)
    build_year = Column(Integer)
    online_since = Column(DateTime(timezone=True))
    with_agent = Column(Boolean)

    def __init__(self):
        self.source = EstateSource.EbayKleinanzeigen
