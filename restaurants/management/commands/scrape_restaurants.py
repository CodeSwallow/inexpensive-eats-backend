from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from restaurants.models import Restaurant, PriceLevel, Category
from restaurants.spiders.restaurant_spider import RestaurantSpider


class Command(BaseCommand):
    help = 'Scrapes restaurants from site and saves them to the database'

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(RestaurantSpider)
        process.start()

    def process_item(self, item):
        price_level = self.get_or_create_price_level(item['price_range'])
        category, _ = Category.objects.get_or_create(name=item['category_name'])
        restaurant, created = Restaurant.objects.get_or_create(
            name=item['name'],
            defaults={
                'price_level': price_level,
                'description': item.get('description', ''),
            }
        )
        restaurant.categories.add(category)
        if not created:
            restaurant.price_level = price_level
            restaurant.description = item.get('description', '')
            restaurant.save()

    def get_or_create_price_level(self, price_range):
        try:
            average_price = Decimal(price_range.replace('mxn', '').strip())
        except (ValueError, DecimalException):
            self.stderr.write(self.style.ERROR(f'Invalid price range format: {price_range}'))
            return None

        price_levels = PriceLevel.objects.all()
        for price_level in price_levels:
            if price_level.min_price <= average_price <= price_level.max_price:
                return price_level

        self.stderr.write(self.style.WARNING(f'No price level found for average price {average_price}'))
        return None
