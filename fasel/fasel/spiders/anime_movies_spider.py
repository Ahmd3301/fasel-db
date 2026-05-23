from fasel.spiders.base_spider import FaselBaseSpider

class AnimeMoviesSpider(FaselBaseSpider):
    name     = "anime_movies"
    category = "anime_movies"
    base_url = "https://www.fasel-hd.cam/anime-movies"
