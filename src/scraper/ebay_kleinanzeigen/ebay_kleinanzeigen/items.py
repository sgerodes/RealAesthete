# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EbayKleinanzeigenItem(scrapy.Item):

    price = scrapy.Field()
    area = scrapy.Field()
    postal_code = scrapy.Field()
    url = scrapy.Field()
    exposition_type = scrapy.Field()
    estate_type = scrapy.Field()

    source_id = scrapy.Field()
    rooms = scrapy.Field()
    city = scrapy.Field()
    online_since = scrapy.Field()
