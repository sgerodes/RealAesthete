import configuration  # noinspection Do not delete
import persistence
import logging


logger = logging.getLogger(__name__)


def main():
    # ek = persistence.models.EbayKleinanzeigen()
    # ek.price = 1230
    # ek.area = 23
    #persistence.service.save_estate_entity(ek)
    ans = persistence.service.read_all_ebay_kleinanzeigen()
    logger.debug(ans)


if __name__ == '__main__':
    main()
