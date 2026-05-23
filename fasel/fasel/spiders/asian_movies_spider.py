from fasel.spiders.base_spider import FaselBaseSpider

class AsianMoviesSpider(FaselBaseSpider):
    name     = "asian_movies"
    category = "asian_movies"
    base_url = "https://www.fasel-hd.cam/asian-movies"
