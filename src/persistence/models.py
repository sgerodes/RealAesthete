import sqlalchemy
import logging
import datetime
from src.persistence import enums
from .. import scrapers
from sqlalchemy.ext.declarative import declarative_base
from . import utils
from functools import lru_cache
import inflection

logger = logging.getLogger(__name__)
#Base = declarative_base()


class Base(declarative_base()):
    __abstract__ = True

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    @utils.cached_classproperty
    def __tablename__(cls):
        # return cls.__name__
        # return inflection.tableize(cls.__name__)
        return inflection.underscore(cls.__name__)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'


class EstateBase(Base):
    __abstract__ = True
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow, index=True)


class EbayKleinanzeigen(EstateBase):
    source = sqlalchemy.Column(sqlalchemy.Enum(enums.EstateSource), index=True, default=enums.EstateSource.EbayKleinanzeigen)

    exposition_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.ExpositionType), index=True)
    estate_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.EstateType), index=True)
    price = sqlalchemy.Column(sqlalchemy.Float, index=True)
    area = sqlalchemy.Column(sqlalchemy.Float, index=True)
    postal_code = sqlalchemy.Column(sqlalchemy.String(5), index=True)
    # url = sqlalchemy.Column(sqlalchemy.String)

    source_id = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    rooms = sqlalchemy.Column(sqlalchemy.Float, index=True)
    city = sqlalchemy.Column(sqlalchemy.String)
    online_since = sqlalchemy.Column(sqlalchemy.DateTime, index=True)

    def get_full_url(self):
        # works both
        return 'https://www.ebay-kleinanzeigen.de/s-anzeige/' + self.source_id
        # return 'https://www.ebay-kleinanzeigen.de/' + self.url

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} source_id={self.source_id} price={self.price} area={self.area})'


class Immonet(EstateBase):
    source = sqlalchemy.Column(sqlalchemy.Enum(enums.EstateSource), index=True, default=enums.EstateSource.Immonet)

    exposition_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.ExpositionType), index=True, nullable=True)
    estate_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.EstateType), index=True, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    area = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    postal_code = sqlalchemy.Column(sqlalchemy.String(5), index=True, nullable=True) # cant get postal code from the search page

    source_id = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True, index=True)
    rooms = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    foreclosure = sqlalchemy.Column(sqlalchemy.Boolean)

    def get_full_url(self):
        return 'https://www.immonet.de/angebot/' + self.source_id

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} source_id={self.source_id} price={self.price} area={self.area} ' \
               f'postal_code={self.postal_code})'


class AbstractImmonetDetailed(EstateBase):
    __abstract__ = True
    #owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(f'{Immonet.__tablename__}.id'), unique=True)
    source_id = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True, index=True)
    postal_code = sqlalchemy.Column(sqlalchemy.String(5), index=True, nullable=True)

    @sqlalchemy.ext.declarative.declared_attr
    def owner_id(cls):
        return sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(f'{Immonet.__tablename__}.id'), unique=True)

#
# class ImmonetRentDetailed(AbstractImmonetDetailed):
#     # Miete zzgl. NK
#     cold_rent = sqlalchemy.Column(sqlalchemy.Float)
#     # Miete inkl. NK
#     warm_rent = sqlalchemy.Column(sqlalchemy.Float)
#     # Nebenkosten
#     extra_costs = sqlalchemy.Column(sqlalchemy.Float)
#     # Heizkosten in Nebenkosten enthalten
#     heating_costs_included = sqlalchemy.Column(sqlalchemy.Boolean)
#     # Kaution
#     deposit = sqlalchemy.Column(sqlalchemy.Float)
#     # Baujahr
#     build_year = sqlalchemy.Column(sqlalchemy.Integer)
#     # Verfügbar ab
#     available_from = sqlalchemy.Column(sqlalchemy.Date)
#     # Energieeffizienzklasse
#     energy_efficiency_class = sqlalchemy.Column(sqlalchemy.Enum(enums.EnergyEfficiencyClass), index=True)
#     # Endenergieverbrauch kWh/(m²*a)
#     energy_consumption = sqlalchemy.Column(sqlalchemy.Float)
#     # Etage
#     floor = sqlalchemy.Column(sqlalchemy.Integer)
#     # Balkon
#     balcony = sqlalchemy.Column(sqlalchemy.Boolean)
#     # Keller
#     cellar = sqlalchemy.Column(sqlalchemy.Boolean)
#     # Personenaufzug
#     elevator = sqlalchemy.Column(sqlalchemy.Boolean)
#
#     def get_full_url(self):
#         return 'https://www.immonet.de/angebot/' + self.source_id
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}({self.id} source_id={self.source_id} owner_id={self.owner_id} postal_code={self.postal_code})'


class Immowelt(EstateBase):
    source = sqlalchemy.Column(sqlalchemy.Enum(enums.EstateSource), index=True, default=enums.EstateSource.Immowelt)

    exposition_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.ExpositionType), index=True, nullable=True)
    estate_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.EstateType), index=True, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    area = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    postal_code = sqlalchemy.Column(sqlalchemy.String(5), index=True, nullable=True)

    source_id = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True, index=True)
    rooms = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def get_full_url(self):
        return 'https://www.immowelt.de/expose/' + self.source_id

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} source_id={self.source_id} price={self.price} area={self.area})'


# class ImmoweltPostalCode(Base):
#     __tablename__ = 'ImmoweltPostalCode'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
#     postal_code = sqlalchemy.Column(sqlalchemy.String(5), index=True, nullable=False, unique=True)
#     exists = sqlalchemy.Column(sqlalchemy.Boolean, index=True, nullable=False, default=True)
#
#     created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
#     updated_at = sqlalchemy.Column(sqlalchemy.DateTime, index=True)
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}({self.id} postal_code={self.postal_code} exists={self.exists})'


class ImmoweltPostalCodeStatistics(Base):
    __table_args__ = (
        sqlalchemy.UniqueConstraint('postal_code', 'exposition_type', 'estate_type'),
    )

    postal_code = sqlalchemy.Column(sqlalchemy.String(5), index=True, nullable=False)
    exposition_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.ExpositionType), index=True, nullable=False)
    estate_type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.EstateType), index=True, nullable=False)

    total_entries = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    last_search = sqlalchemy.Column(sqlalchemy.DateTime)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} postal_code={self.postal_code} ' \
               f'exposition_type={self.exposition_type}, estate_type={self.estate_type}, ' \
               f'total_entries={self.total_entries}, last_search={self.last_search})'


class PersistencePipelineStats(Base):
    name = sqlalchemy.Column(sqlalchemy.String(20), index=True, nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
    type = sqlalchemy.Column(sqlalchemy.Enum(scrapers.enums.PersistencePipelineStats), index=True, nullable=False)
    rate = sqlalchemy.Column(sqlalchemy.Integer, nullable=False) # microseconds timedelta

    def set_rate_from_timedelta(self, td: datetime.timedelta):
        self.rate = td.microseconds

    def set_type_reading(self):
        self.type = scrapers.enums.PersistencePipelineStats.READING

    def set_type_creation(self):
        self.type = scrapers.enums.PersistencePipelineStats.CREATION
