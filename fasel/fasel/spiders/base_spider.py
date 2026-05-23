import scrapy
import json
import os
from fasel.items import FaselItem

# المسار المطلق لمجلد data/ بالنسبة لهذا الملف
# الملف في: fasel/fasel/spiders/base_spider.py
# data/  في: data/  (بجانب مجلد fasel/)
_HERE = os.path.dirname(os.path.abspath(__file__))          # .../fasel/fasel/spiders
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "data"))  # .../data


class FaselBaseSpider(scrapy.Spider):
    """
    Base spider مشترك لكل الـ 8 فئات.

    المنطق:
      ┌─ data/category.json غير موجود ─→ FULL CRAWL
      └─ موجود                         ─→ SMART MODE

    Selectors مؤكدة من HTML الموقع:
      container : #postList .postDiv
      link      : a::attr(href)
      name      : img::attr(alt)  أو  .h1::text
      img       : img::attr(data-src)  ثم  img::attr(src)
    """

    base_url = ""
    category = ""

    def start_requests(self):
        self.db_path       = os.path.join(_ROOT, f"{self.category}.json")
        self.is_full_crawl = not os.path.exists(self.db_path)
        self.seen_links    = set()

        self.logger.info(f"[{self.category}] db_path = {self.db_path}")
        self.logger.info(f"[{self.category}] is_full_crawl = {self.is_full_crawl}")

        if not self.is_full_crawl:
            with open(self.db_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
            # لو الملف موجود لكن فارغ [] → full crawl أيضاً
            if not data:
                self.is_full_crawl = True
                self.logger.info(f"[{self.category}] الملف فارغ → full crawl")
            else:
                self.seen_links = {item["link"] for item in data}
                self.logger.info(
                    f"[{self.category}] وضع المقارنة — {len(self.seen_links)} عمل موجود"
                )
        else:
            self.logger.info(f"[{self.category}] أول تشغيل — سحب كامل")

        yield scrapy.Request(
            url=f"{self.base_url}/page/1",
            callback=self.parse,
            meta={"page": 1},
        )

    def parse(self, response):
        page  = response.meta["page"]
        cards = response.css("#postList .postDiv")

        self.logger.info(
            f"[{self.category}] page/{page} — وجد {len(cards)} كارد"
        )

        if not cards:
            self.logger.info(f"[{self.category}] انتهت الصفحات عند page/{page}")
            return

        new_count = 0

        for card in cards:
            href = card.css("a::attr(href)").get("")
            link = response.urljoin(href) if href else ""
            if not link:
                continue

            img = (
                card.css("a img::attr(data-src)").get() or
                card.css("a img::attr(src)").get() or ""
            )

            name = (
                card.css("a img::attr(alt)").get("").strip() or
                card.css(".h1::text").get("").strip()
            )

            if not self.is_full_crawl and link in self.seen_links:
                continue

            new_count += 1
            yield FaselItem(
                name=name,
                img=img,
                link=link,
                category=self.category,
            )

        self.logger.info(f"[{self.category}] page/{page} — جديد: {new_count}")

        if self.is_full_crawl or new_count > 0:
            yield scrapy.Request(
                url=f"{self.base_url}/page/{page + 1}",
                callback=self.parse,
                meta={"page": page + 1},
            )
        else:
            self.logger.info(
                f"[{self.category}] توقف ذكي عند page/{page} — كل المحتوى قديم"
            )
