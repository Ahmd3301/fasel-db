import scrapy
import json
import os
from fasel.items import FaselItem

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "data"))


class FaselBaseSpider(scrapy.Spider):

    base_url  = ""
    category  = ""
    start_urls = ["http://placeholder.invalid"]  # مطلوب لـ Scrapy 2.16

    def start_requests(self):
        self.db_path       = os.path.join(_ROOT, f"{self.category}.json")
        self.is_full_crawl = not os.path.exists(self.db_path)
        self.seen_links    = set()

        self.logger.info(f"[{self.category}] start_requests called ✓")
        self.logger.info(f"[{self.category}] db_path = {self.db_path}")
        self.logger.info(f"[{self.category}] is_full_crawl = {self.is_full_crawl}")

        if not self.is_full_crawl:
            with open(self.db_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
            if not data:
                self.is_full_crawl = True
            else:
                self.seen_links = {item["link"] for item in data}
                self.logger.info(
                    f"[{self.category}] وضع المقارنة — {len(self.seen_links)} عمل"
                )

        target = f"{self.base_url}/page/1"
        self.logger.info(f"[{self.category}] → {target}")

        yield scrapy.Request(
            url=target,
            callback=self.parse,
            meta={"page": 1},
            dont_filter=True,
        )

    def parse(self, response):
        page  = response.meta["page"]
        cards = response.css("#postList .postDiv")

        self.logger.info(
            f"[{self.category}] page/{page} "
            f"status={response.status} cards={len(cards)}"
        )

        if not cards:
            self.logger.info(
                f"[{self.category}] HTML[500]: "
                f"{response.text[:500].replace(chr(10),' ')}"
            )
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
            yield FaselItem(name=name, img=img, link=link, category=self.category)

        self.logger.info(f"[{self.category}] page/{page} — جديد: {new_count}")

        if self.is_full_crawl or new_count > 0:
            yield scrapy.Request(
                url=f"{self.base_url}/page/{page + 1}",
                callback=self.parse,
                meta={"page": page + 1},
                dont_filter=True,
            )
        else:
            self.logger.info(f"[{self.category}] توقف ذكي عند page/{page}")
