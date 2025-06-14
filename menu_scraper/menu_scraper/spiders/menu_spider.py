import scrapy


class MenuSpiderSpider(scrapy.Spider):
    name = "menu_spider"
    allowed_domains = ["www.mcdonalds.com"]
    start_urls = ["https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"]

    def parse(self, response):
        self.logger.info(f"Parsing main page: {response.url}")
        item_links = response.css("li.cmp-category__item a::attr(href)").getall()

        for link in item_links:
            yield response.follow(link, callback=self.parse_product)


    def parse_product(self, response):
        self.logger.info(f"Parsing product page: {response.url}")

        yield {
            "name": response.css("h1.product-title::text").get(),
            "description": response.css("span.price::text").get(),
            "calories": response.css("span.sku::text").get(),
            "fats": response.css("div.description::text").get(),
            "carbs": response.css("span.availability::text").get(),
            "protein": response.url,
            "unsaturated_fats": response.url,
            "sugar": response.url,
            "portion": response.url,
        }