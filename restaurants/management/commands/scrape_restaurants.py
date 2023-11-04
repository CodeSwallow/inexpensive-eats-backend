from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess

from restaurants.spiders.retaurant_spider import RestaurantSpider


class Command(BaseCommand):
    help = 'Scrapes restaurants from restaurant website'

    def handle(self, *args, **options):
        process = CrawlerProcess({
            'BOT_NAME': 'restaurant_scraper',
            'SPIDER_MODULES': ['restaurants.spiders'],
            'NEWSPIDER_MODULE': 'restaurants.spiders',
            'ITEM_PIPELINES': {
                'restaurants.pipelines.RestaurantPipeline': 300,
            },
        })
        process.crawl(RestaurantSpider)
        process.start()
