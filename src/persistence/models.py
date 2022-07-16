import sqlalchemy
import logging
from src.persistence import enums
from .. import scrapers
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)
Base = declarative_base()


class EbayKleinanzeigen(Base):
    __tablename__ = 'EbayKleinanzeigen'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    source = sqlalchemy.Column(sqlalchemy.Enum(enums.EstateSource), index=True, default=enums.EstateSource.EbayKleinanzeigen)

    exposition_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.ExpositionType), index=True)
    estate_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.EstateType), index=True)
    price = sqlalchemy.Column(sqlalchemy.Numeric(precision=2))
    area = sqlalchemy.Column(sqlalchemy.Float)
    postal_code = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    url = sqlalchemy.Column(sqlalchemy.String)

    source_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    rooms = sqlalchemy.Column(sqlalchemy.Float)
    city = sqlalchemy.Column(sqlalchemy.String)
    online_since = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))

    def get_full_url(self):
        return 'https://www.ebay-kleinanzeigen.de/' + self.url

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} price={self.price} area={self.area})'


class Immonet(Base):
    __tablename__ = 'Immonet'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    source = sqlalchemy.Column(sqlalchemy.Enum(enums.EstateSource), index=True, default=enums.EstateSource.Immonet)

    exposition_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.ExpositionType), index=True)
    estate_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.EstateType), index=True)
    price = sqlalchemy.Column(sqlalchemy.Numeric(precision=2))
    area = sqlalchemy.Column(sqlalchemy.Float)
    postal_code = sqlalchemy.Column(sqlalchemy.Integer, index=True)

    source_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    rooms = sqlalchemy.Column(sqlalchemy.Float)
    city = sqlalchemy.Column(sqlalchemy.String)

    foreclosure = sqlalchemy.Column(sqlalchemy.Boolean)

    def get_full_url(self):
        return 'https://www.immonet.de/angebot/' + self.source_id

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} price={self.price} area={self.area})'