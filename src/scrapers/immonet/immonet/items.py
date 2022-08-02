import scrapy


class ImmonetItem(scrapy.Item):
    price = scrapy.Field()
    area = scrapy.Field()
    postal_code = scrapy.Field()
    url = scrapy.Field()
    exposition_type = scrapy.Field()
    estate_type = scrapy.Field()

    source_id = scrapy.Field()
    rooms = scrapy.Field()
    city = scrapy.Field()

    foreclosure = scrapy.Field()
