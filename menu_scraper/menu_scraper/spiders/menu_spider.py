import scrapy
import json
import re

from scrapy.http import Response, Request
from typing import Any, Generator


class MenuSpiderSpider(scrapy.Spider):
    name = "menu_spider"
    allowed_domains = ["www.mcdonalds.com"]
    start_urls = ["https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"]

    def parse(self, response: Response) -> Generator[Request, None, None]:
        self.logger.info(f"Parsing main page: {response.url}")
        item_links = response.css("li.cmp-category__item a::attr(href)").getall()

        self.logger.info(f"Found {len(item_links)} links on menu page")

        seen_ids = set()
        for link in item_links:
            match = re.search(r"/product/(\d+)", link)
            if match:
                item_id = int(match.group(1))
                if item_id not in seen_ids:
                    seen_ids.add(item_id)
                    api_url = (
                        f"https://www.mcdonalds.com/dnaapp/itemDetails"
                        f"?country=UA&language=uk&showLiveData=true&item={item_id}"
                    )
                    yield scrapy.Request(
                        api_url,
                        callback=self.parse_product,
                        cb_kwargs={"item_id": item_id},
                    )

    def parse_product(
        self, response: Response, item_id: int | None = None
    ) -> Generator[dict[str, Any], None, None]:
        self.logger.info(f"Parsing API response for item_id={item_id}")

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error for item {item_id}: {e}")
            return

        item = data.get("item", {})

        name = item.get("item_name")
        if not name:
            self.logger.warning(f"Item {item_id} skipped: no name found.")
            return

        try:
            raw_description = item.get("description", "")
            description = re.sub(r'[\r\n"]+', " ", raw_description).strip()
            description = re.sub(r"\s{2,}", " ", description)
        except (AttributeError, TypeError) as e:
            self.logger.warning(f"Failed to clean description for item {item_id}: {e}")
            description = None

        try:
            nutrients_raw = item.get("nutrient_facts", {}).get("nutrient", [])
            nutrients = {n["name"]: n["value"] for n in nutrients_raw}
        except (KeyError, TypeError) as e:
            self.logger.warning(f"Failed to parse nutrients for item {item_id}: {e}")
            nutrients = {}

        yield {
            "name": name,
            "description": description or None,
            "portion": nutrients.get("Вага порції"),
            "calories": nutrients.get("Калорійність"),
            "fats": nutrients.get("Жири"),
            "unsaturated_fats": nutrients.get("НЖК"),
            "carbs": nutrients.get("Вуглеводи"),
            "sugar": nutrients.get("Цукор"),
            "protein": nutrients.get("Білки"),
            "salt": nutrients.get("Сіль"),
        }
