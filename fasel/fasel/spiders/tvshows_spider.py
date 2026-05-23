from fasel.spiders.base_spider import FaselBaseSpider

class TvShowsSpider(FaselBaseSpider):
    name     = "tvshows"
    category = "tvshows"
    base_url = "https://www.fasel-hd.cam/tvshows"
