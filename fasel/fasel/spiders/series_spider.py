from fasel.spiders.base_spider import FaselBaseSpider

class SeriesSpider(FaselBaseSpider):
    name     = "series"
    category = "series"
    base_url = "https://www.fasel-hd.cam/series"
