import logging
from .generic import Repository
from typing import Optional
from .models import EbayKleinanzeigen, Immonet, Immowelt, ImmoweltPostalCodeStatistics
from .. import scrapers


logger = logging.getLogger(__name__)


class EbayKleinanzeigenRepository(Repository[EbayKleinanzeigen]):
    @classmethod
    def read_by_source_id(cls, source_id: int) -> Optional[EbayKleinanzeigen]:
        return cls.read_by_unique(source_id=source_id)


class ImmonetRepository(Repository[Immonet]):
    @classmethod
    def read_by_source_id(cls, source_id: str) -> Optional[Immonet]:
        return cls.read_by_unique(source_id=source_id)


class ImmoweltPostalCodeStatisticsRepository(Repository[ImmoweltPostalCodeStatistics]):
    @classmethod
    def read_or_create(cls, postal_code: str,
                       exposition_type: scrapers.enums.ExpositionType,
                       estate_type: scrapers.enums.EstateType) -> ImmoweltPostalCodeStatistics:
        ipcs = cls.read_first(postal_code=postal_code, exposition_type=exposition_type, estate_type=estate_type)
        if not ipcs:
            cls.create_by_unique(postal_code=postal_code, exposition_type=exposition_type, estate_type=estate_type)
        return ipcs

    @classmethod
    def create_by_unique(cls, postal_code: str,
                       exposition_type: scrapers.enums.ExpositionType,
                       estate_type: scrapers.enums.EstateType) -> ImmoweltPostalCodeStatistics:
        return cls.create(ImmoweltPostalCodeStatistics(postal_code=postal_code, exposition_type=exposition_type, estate_type=estate_type))


class ImmoweltRepository(Repository[Immowelt]):
    @classmethod
    def read_by_source_id(cls, source_id: int) -> Optional[Immowelt]:
        return cls.read_by_unique(source_id=source_id)

    @classmethod
    def create(cls, entity: Immowelt) -> Optional[Immowelt]:
        ipcs = ImmoweltPostalCodeStatisticsRepository.read_by_unique(estate_type=entity.estate_type,
                                                              exposition_type=entity.exposition_type,
                                                              postal_code=entity.postal_code)
        ipcs.total_entries = ipcs.total_entries + 1
        ImmoweltPostalCodeStatisticsRepository.update(ipcs)
        return super().create(entity)

#
# class ImmonetRentDetailedRepository(Repository[ImmonetRentDetailed]):
#     pass


# class ImmoweltPostalCodeRepository(Repository[ImmoweltPostalCode]):
#     @classmethod
#     def read_or_create_by_postal_code(cls, postal_code: str) -> Optional[ImmoweltPostalCode]:
#         ipc = cls.read_by_unique(postal_code=postal_code)
#         if not ipc:
#             ipc = ImmoweltPostalCode(postal_code=postal_code)
#             cls.create(ipc)
#         return ipc
#
#     @classmethod
#     def create(cls, immowelt_postal_code: ImmoweltPostalCode) -> ImmoweltPostalCode:
#         if not immowelt_postal_code.postal_code or not len(immowelt_postal_code.postal_code) == 5:
#             logger.error(f'Cant create a postal code {immowelt_postal_code.postal_code}. All postal codes need to be 5 in length')
#             return None
#         super().create(immowelt_postal_code)

