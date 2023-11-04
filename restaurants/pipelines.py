import logging
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist

from restaurants.models import Restaurant, PriceLevel, Category

logger = logging.getLogger(__name__)


class RestaurantPipeline:

    def process_item(self, item, spider):
        price_level = self.get_or_create_price_level(item['price_range'])
        if not price_level:
            logger.warning(f'No PriceLevel created for item: {item}')
            return item

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

        return item

    # noinspection PyMethodMayBeStatic
    def get_or_create_price_level(self, price_range):
        try:
            average_price = Decimal(price_range.replace('mxn', '').strip())
        except DecimalException as e:
            logger.error(f'Invalid price range format: {price_range}')
            return None

        price_levels = PriceLevel.objects.all()
        for price_level in price_levels:
            if price_level.min_price <= average_price <= price_level.max_price:
                return price_level

        logger.warning(f'No price level found for average price {average_price}')
        return None
