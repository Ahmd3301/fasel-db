import json
import os

class FaselPipeline:

    def open_spider(self, spider):
        self.new_items  = []
        self.db_path    = os.path.join("..", "data", f"{spider.category}.json")
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
        # تجاهل المكررات داخل نفس الـ run
        if item["link"] not in self.seen_links:
            self.seen_links.add(item["link"])
            self.new_items.append(dict(item))
        return item

    def close_spider(self, spider):
        # الجديد في المقدمة + القديم بعده
        final = self.new_items + self.existing
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(final, f, ensure_ascii=False, indent=2)
        spider.logger.info(
            f"[{spider.category}] ✅ جديد: {len(self.new_items)} | "
            f"إجمالي: {len(final)}"
        )
