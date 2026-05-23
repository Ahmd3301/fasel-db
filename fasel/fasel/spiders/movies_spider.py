from fasel.spiders.base_spider import FaselBaseSpider

class MoviesSpider(FaselBaseSpider):
    name     = "movies"
    category = "movies"
    base_url = "https://www.fasel-hd.cam/movies"
