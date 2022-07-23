# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImmoweltItem(scrapy.Item):
    price = scrapy.Field()
    area = scrapy.Field()
    rooms = scrapy.Field()
    postal_code = scrapy.Field()
    city = scrapy.Field()
    source_id = scrapy.Field()

    exposition_type = scrapy.Field()
    estate_type = scrapy.Field()



class DetailedImmoweltItem(scrapy.Item):
    Kaltmiete = scrapy.Field()
    Nebenkosten = scrapy.Field()
    Kaution = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    rooms = scrapy.Field()
    postal_code = scrapy.Field()
    city = scrapy.Field()
    source_id = scrapy.Field()

    exposition_type = scrapy.Field()
    estate_type = scrapy.Field()

