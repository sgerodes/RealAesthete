from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from .models.base import engine, EstateSource, Estate
from .models.ebay_kleinanzeigen import EbayKleinanzeigen
from typing import List
import logging


ALL_DEFAULT_LIMIT = 100

logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)
session = Session()


def save_estate_entity(estate: Estate):
    logger.debug(f'saving estate {estate}')
    session.add(estate)
    session.commit()


def save_estate_list(estate_list: List[Estate]):
    logger.debug(f'saving estate list {estate_list}')
    session.add_all(estate_list)
    session.commit()


def read_ebay_kleinanzeigen_by_id(id: int) -> EbayKleinanzeigen:
    return session.query(EbayKleinanzeigen).get(id)


def read_all_ebay_kleinanzeigen(limit=ALL_DEFAULT_LIMIT) -> List[EbayKleinanzeigen]:
    return session.query(EbayKleinanzeigen).limit(limit).all()


def rollback():
    # clears the session
    session.rollback()

