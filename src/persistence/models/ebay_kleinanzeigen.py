from .base import Estate, Base
from sqlalchemy import create_engine, Column, Integer, String


class EbayKleinanzeigen(Base, Estate):
    __tablename__ = 'EbayKleinanzeigen'
    pass
