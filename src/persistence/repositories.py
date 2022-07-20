import logging
from .generic import Repository
from typing import Optional
from .models import EbayKleinanzeigen, Immonet, ImmoweltPostalCode, Immowelt, ImmoweltPostalCodeRequestLog


logger = logging.getLogger(__name__)


class EbayKleinanzeigenRepository(Repository[EbayKleinanzeigen]):
    @classmethod
    def read_by_source_id(cls, source_id: int) -> Optional[EbayKleinanzeigen]:
        logger.debug(f'reading EbayKleinanzeigen by {source_id=}')
        return cls.read_by_unique(source_id=source_id)


class ImmonetRepository(Repository[Immonet]):
    @classmethod
    def read_by_source_id(cls, source_id: int) -> Optional[Immonet]:
        logger.debug(f'reading Immonet by {source_id=}')
        return cls.read_by_unique(source_id=source_id)


class ImmoweltRepository(Repository[Immowelt]):
    @classmethod
    def read_by_source_id(cls, source_id: int) -> Optional[Immowelt]:
        logger.debug(f'reading Immowelt by {source_id=}')
        return cls.read_by_unique(source_id=source_id)


class ImmoweltPostalCodeRepository(Repository[ImmoweltPostalCode]):
    @classmethod
    def read_or_create_by_postal_code(cls, postal_code: str) -> Optional[ImmoweltPostalCode]:
        ipc = cls.read_by_unique(postal_code=postal_code)
        if not ipc:
            ipc = ImmoweltPostalCode(postal_code=postal_code)
            cls.create(ipc)
        return ipc

    @classmethod
    def create(cls, immowelt_postal_code: ImmoweltPostalCode) -> Optional[ImmoweltPostalCode]:
        if not immowelt_postal_code.postal_code or not len(immowelt_postal_code.postal_code) == 5:
            logger.error(f'Cant create a postal code {immowelt_postal_code.postal_code}. All postal codes need to be 5 in length')
            return None
        super().create(immowelt_postal_code)


class ImmoweltPostalCodeRequestLogRepository(Repository[ImmoweltPostalCodeRequestLog]):
    pass
