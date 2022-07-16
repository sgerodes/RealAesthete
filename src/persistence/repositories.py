import logging
from .generic import Repository
from .models import EbayKleinanzeigen


logger = logging.getLogger(__name__)


class EbayKleinanzeigenRepository(Repository[EbayKleinanzeigen]):
    @classmethod
    def read_by_source_id(cls, source_id: int) -> EbayKleinanzeigen:
        logger.debug(f'reading EbayKleinanzeigen by {source_id=}')
        return cls.read_by_unique(source_id)


