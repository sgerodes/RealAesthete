# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImmoweltItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source_id = scrapy.Field() # https://www.immowelt.de/expose/2zc2r3k
    pass
