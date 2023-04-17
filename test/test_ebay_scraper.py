import datetime

from src.scrapers.ebay_kleinanzeigen.run import get_spider_and_settings
import scrapy
import unittest
from unittest.mock import MagicMock
import os



def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


class TestEbayKleinanzeigenSpider(unittest.TestCase):
    def test_parse(self):
        file_path = 'resources/examples/ebay_kleinanzeigen/ebay_flat_rent_2023_04_13.html'
        # file_path = 'resources/examples/ebay_kleinanzeigen/ebay.html'
        file_url = f"file://{os.path.abspath(file_path)}"  # Convert the file path to a file URL
        response = scrapy.http.TextResponse(url=file_url, body=read_text_file(file_path), encoding='utf-8')

        dummy_request = scrapy.Request(file_url, dont_filter=True)
        response.request = dummy_request

        spiders_and_settings = get_spider_and_settings()
        SpiderClass = spiders_and_settings.pop()[0]
        for item in SpiderClass().parse(response):
            if isinstance(item, scrapy.Request):
                continue
            if isinstance(item, scrapy.Item):
                print(item)
                if item.city == "Höchenschwand":
                    assert item.source_id == "2408874930"
                    assert item.postal_code == "79862"
                    assert item.city == "Höchenschwand"
                    assert item.area == "220"
                    assert item.rooms == "5"
                    assert item.price == "1400"

                if item.source_id == "2413558036":
                    assert item.city == "Holzkirchen Unterfranken"
                    assert item.price == "680"
                    assert item.online_since == datetime.datetime.combine(datetime.date.today(), datetime.time.fromisoformat("13:43"))



