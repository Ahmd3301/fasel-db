import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))       # .../fasel/fasel
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", "data"))  # .../data


class FaselPipeline:

    def open_spider(self, spider):
        self.new_items  = []
        self.db_path    = os.path.join(_ROOT, f"{spider.category}.json")
        self.existing   = []
        self.seen_links = set()

        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as f:
                try:
                    self.existing = json.load(f)
                except json.JSONDecodeError:
                    self.existing = []
            self.seen_links = {item["link"] for item in self.existing}

    def process_item(self, item, spider):
        if item["link"] not in self.seen_links:
            self.seen_links.add(item["link"])
            self.new_items.append(dict(item))
        return item

    def close_spider(self, spider):
        final = self.new_items + self.existing
        os.makedirs(_ROOT, exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(final, f, ensure_ascii=False, indent=2)
        spider.logger.info(
            f"[{spider.category}] ✅ جديد: {len(self.new_items)} | إجمالي: {len(final)}"
        )
