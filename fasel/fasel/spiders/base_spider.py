import scrapy
import json
import os
from fasel.items import FaselItem


class FaselBaseSpider(scrapy.Spider):
    """
    Base spider مشترك لكل الـ 8 فئات.

    المنطق:
      ┌─ data/category.json غير موجود ─→ FULL CRAWL (كل الصفحات)
      └─ موجود                         ─→ SMART MODE (توقف عند أول صفحة كلها قديمة)

    الـ Selectors (مستخرجة من sp.cjs):
      container : #postList .postDiv
      link      : a:first  →  href
      name      : img[alt]  أو  .h1::text
      img       : img[data-src]  ثم  img[src]   (lazy-load aware)
    """

    base_url = ""   # يُحدَّد في كل spider فرعي
    category = ""

    # ── بداية الـ Spider ──────────────────────────────────────
    def start_requests(self):
        self.db_path      = os.path.join("..", "data", f"{self.category}.json")
        self.is_full_crawl = not os.path.exists(self.db_path)
        self.seen_links   = set()

        if not self.is_full_crawl:
            with open(self.db_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
            self.seen_links = {item["link"] for item in data}
            self.logger.info(
                f"[{self.category}] 🔄 وضع المقارنة — "
                f"{len(self.seen_links)} عمل موجود"
            )
        else:
            self.logger.info(
                f"[{self.category}] 🚀 أول تشغيل — سحب كامل لكل الصفحات"
            )

        yield scrapy.Request(
            url=f"{self.base_url}/page/1",
            callback=self.parse,
            meta={"page": 1},
        )

    # ── معالجة كل صفحة ───────────────────────────────────────
    def parse(self, response):
        page  = response.meta["page"]
        cards = response.css("#postList .postDiv")

        # صفحة فاضية = انتهت الصفحات
        if not cards:
            self.logger.info(
                f"[{self.category}] 🏁 انتهت الصفحات عند page/{page}"
            )
            return

        new_count = 0

        for card in cards:
            anchor = card.css("a").attrib.get("href", "")
            link   = response.urljoin(anchor) if anchor else ""
            if not link:
                continue

            # img: data-src أولاً (lazy-load) ثم src
            img_tag = card.css("a img")
            img     = (
                img_tag.attrib.get("data-src") or
                img_tag.attrib.get("src") or ""
            )

            # name: alt أولاً ثم .h1
            name = (
                img_tag.attrib.get("alt", "").strip() or
                card.css(".h1::text").get("").strip()
            )

            # ── وضع المقارنة: تخطي القديم ─────────────────
            if not self.is_full_crawl and link in self.seen_links:
                continue

            new_count += 1
            yield FaselItem(
                name=name,
                img=img,
                link=link,
                category=self.category,
            )

        self.logger.info(
            f"[{self.category}] 📄 page/{page} — جديد: {new_count}"
        )

        # ── قرار الاستمرار ────────────────────────────────
        # Full crawl  → كمّل دائماً
        # Smart mode  → توقف لو كل الصفحة قديمة (new_count == 0)
        if self.is_full_crawl or new_count > 0:
            yield scrapy.Request(
                url=f"{self.base_url}/page/{page + 1}",
                callback=self.parse,
                meta={"page": page + 1},
            )
        else:
            self.logger.info(
                f"[{self.category}] ✋ توقف ذكي عند page/{page} "
                f"— كل المحتوى قديم"
            )
