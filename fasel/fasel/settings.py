BOT_NAME = "fasel"

SPIDER_MODULES   = ["fasel.spiders"]
NEWSPIDER_MODULE = "fasel.spiders"

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY           = 0.75
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS      = 4

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

DEFAULT_REQUEST_HEADERS = {
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ar-AR,ar;q=0.9,en;q=0.8",
}

ITEM_PIPELINES = {
    "fasel.pipelines.FaselPipeline": 300,
}

# تعطيل StartSpiderMiddleware فقط
SPIDER_MIDDLEWARES = {
    "scrapy.spidermiddlewares.start.StartSpiderMiddleware": None,
}

LOG_LEVEL        = "INFO"
FEEDS            = {}
RETRY_TIMES      = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
DOWNLOAD_TIMEOUT = 20
