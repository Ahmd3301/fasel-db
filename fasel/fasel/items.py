import scrapy

class FaselItem(scrapy.Item):
    name     = scrapy.Field()
    img      = scrapy.Field()
    link     = scrapy.Field()
    category = scrapy.Field()
