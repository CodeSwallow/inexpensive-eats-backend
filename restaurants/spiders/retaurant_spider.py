import os

import scrapy

from decimal import Decimal


class RestaurantSpider(scrapy.Spider):
    name = 'restaurant_spider'
    allowed_domains = os.getenv('RESTAURANT_SPIDER_ALLOWED_DOMAINS').split(',')
    start_urls = os.getenv('RESTAURANT_SPIDER_URLS').split(',')

    def parse(self, response, **kwargs):
        restaurant_containers = response.css('div[id^="item-restaurante-"]')

        for restaurant_selector in restaurant_containers:
            name = restaurant_selector.css('div.nombre-restaurante a::text').get(default='').strip()
            price_range = restaurant_selector.css('span[itemprop="priceRange"]::text').get(default='').strip()
            category_name = restaurant_selector.css('div.txt100[itemprop="servesCuisine"]::text').get(
                default='').strip()
            description = restaurant_selector.css('p.descripcion-restaurante::text').get(default='').strip()

            if name and price_range and category_name:
                yield {
                    'name': name,
                    'price_range': price_range,
                    'category_name': category_name,
                    'description': description,
                }
            else:
                self.log(f'Missing data in restaurant: {name or "Unknown"}, URL: {response.url}')
