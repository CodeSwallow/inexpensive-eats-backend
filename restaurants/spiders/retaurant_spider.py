import scrapy

from decimal import Decimal

from django.db import transaction

from restaurants.models import Restaurant, PriceLevel


class RestaurantSpider(scrapy.Spider):
    name = 'restaurant_spider'
    allowed_domains = ['zonaturistica.com']
    start_urls = ['https://www.zonaturistica.com/restaurantes/puebla/puebla']

    def parse(self, response, **kwargs):
        price_levels = PriceLevel.objects.all()
        restaurant_containers = response.css('div[id^="item-restaurante-"]')

        for restaurant_selector in restaurant_containers:
            name = restaurant_selector.css('div.nombre-restaurante a::text').get()

            if not name:
                self.log('No name found for restaurant')
                continue

            price_range = restaurant_selector.css('span[itemprop="priceRange"]::text').get()
            category_name = restaurant_selector.css('div.txt100[itemprop="servesCuisine"]::text').get()
            description = restaurant_selector.css('p.descripcion-restaurante::text').get()

            if price_range:
                average_price = Decimal(price_range.replace('mxn', '').strip())
                price_level = self.get_price_level(average_price, price_levels)
            else:
                self.log(f'No price range found for {name}')
                continue

            if not category_name:
                self.log(f'No category name found for {name}')
                continue

            category, _ = Category.objects.get_or_create(name=category_name)

            with transaction.atomic():
                restaurant, created = Restaurant.objects.get_or_create(
                    name=name,
                    defaults={
                        'price_level': price_level,
                        'description': description
                    }
                )

                restaurant.categories.add(category)

                if not created:
                    restaurant.price_level = price_level
                    restaurant.description = description
                    restaurant.save()

    def get_price_level(self, average_price, price_levels):
        for price_level in price_levels:
            if price_level.min_price <= average_price <= price_level.max_price:
                return price_level
        self.log(f'No price level found for average price {average_price}')
        return None
