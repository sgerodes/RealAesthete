from src.parsers.scrapy2db_parsers import *
from src.scrapers.ebay_kleinanzeigen.ebay_kleinanzeigen.items import *
from src.scrapers.immonet.immonet.items import *
from src.scrapers.immowelt.immowelt.items import *
from src.scrapers.enums import *
import datetime
import os
from scrapy_dot_items import dot_items_globally


dot_items_globally()


def test_ebay_parser():
    item = EbayKleinanzeigenItem()
    item.price = 10000.00
    item.area = 43.56
    item.postal_code = "80432"
    item.url = "https://www.ebay-kleinanzeigen.de/s-anzeige/zwei-zimmerwohnung/2166569366-203-1699"
    item.exposition_type = ExpositionType.BUY
    item.estate_type = EstateType.FLAT

    item.source_id = "166569366"
    item.rooms = 3
    item.city = "München"
    item.online_since = datetime.datetime(year=2022, month=5, day=1)

    db_model = EbayKleinanzeigenParser.create_from_scrapy_item(item)
    assert db_model.price == item.price
    assert db_model.area == item.area
    assert db_model.postal_code == item.postal_code
    assert db_model.url == item.url
    assert db_model.exposition_type == item.exposition_type
    assert db_model.estate_type == item.estate_type
    assert db_model.source_id == item.source_id
    assert db_model.rooms == item.rooms
    assert db_model.city == item.city
    assert db_model.online_since == item.online_since


def test_immonet_parser():
    item = ImmonetItem()
    item.price = 10000.00
    item.area = 43.56
    item.postal_code = "80432"
    item.exposition_type = ExpositionType.BUY
    item.estate_type = EstateType.FLAT

    item.source_id = "166569366"
    item.rooms = 3
    item.city = "München"
    item.foreclosure = True

    db_model = ImmonetParser.create_from_scrapy_item(item)
    assert db_model.price == item.price
    assert db_model.area == item.area
    assert db_model.postal_code == item.postal_code
    assert db_model.exposition_type == item.exposition_type
    assert db_model.estate_type == item.estate_type
    assert db_model.source_id == item.source_id
    assert db_model.rooms == item.rooms
    assert db_model.city == item.city
    assert db_model.foreclosure == item.foreclosure


def test_immowelt_parser():
    item = ImmoweltItem()
    item.price = 10000.00
    item.area = 43.56
    item.postal_code = "80432"
    item.exposition_type = ExpositionType.BUY
    item.estate_type = EstateType.FLAT

    item.source_id = "166569366"
    item.rooms = 3
    item.city = "München"

    db_model = ImmoweltParser.create_from_scrapy_item(item)
    assert db_model.price == item.price
    assert db_model.area == item.area
    assert db_model.postal_code == item.postal_code
    assert db_model.exposition_type == item.exposition_type
    assert db_model.estate_type == item.estate_type
    assert db_model.source_id == item.source_id
    assert db_model.rooms == item.rooms
    assert db_model.city == item.city
