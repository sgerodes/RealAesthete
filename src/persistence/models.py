import sqlalchemy
import logging
import datetime
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
    price = sqlalchemy.Column(sqlalchemy.Numeric(precision=2), index=True)
    area = sqlalchemy.Column(sqlalchemy.Float, index=True)
    postal_code = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    url = sqlalchemy.Column(sqlalchemy.String)

    source_id = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    rooms = sqlalchemy.Column(sqlalchemy.Float, index=True)
    city = sqlalchemy.Column(sqlalchemy.String)
    online_since = sqlalchemy.Column(sqlalchemy.DateTime, index=True)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow, index=True)

    def get_full_url(self):
        return 'https://www.ebay-kleinanzeigen.de/' + self.url

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} price={self.price} area={self.area})'


class Immonet(Base):
    __tablename__ = 'Immonet'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    source = sqlalchemy.Column(sqlalchemy.Enum(enums.EstateSource), index=True, default=enums.EstateSource.Immonet)

    exposition_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.ExpositionType), index=True, nullable=True)
    estate_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.EstateType), index=True, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Numeric(precision=2), nullable=True, index=True)
    area = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    postal_code = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True)

    source_id = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True, index=True)
    rooms = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    foreclosure = sqlalchemy.Column(sqlalchemy.Boolean)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow, index=True)

    def get_full_url(self):
        return 'https://www.immonet.de/angebot/' + self.source_id

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} price={self.price} area={self.area})'


class Immowelt(Base):
    __tablename__ = 'Immowelt'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    source = sqlalchemy.Column(sqlalchemy.Enum(enums.EstateSource), index=True, default=enums.EstateSource.Immowelt)

    exposition_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.ExpositionType), index=True, nullable=True)
    estate_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.EstateType), index=True, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Numeric(precision=2), nullable=True, index=True)
    area = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    postal_code = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True)

    source_id = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True, index=True)
    rooms = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow, index=True)

    def get_full_url(self):
        return 'https://www.immowelt.de/expose/' + self.source_id

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} price={self.price} area={self.area})'


def ImmoweltZipCode(Base):
    __tablename__ = 'ImmoweltZipCode'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    postal_code = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False, unique=False)
    exists = sqlalchemy.Column(sqlalchemy.Boolean, index=True, nullable=False, default=True)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow, index=True)

    