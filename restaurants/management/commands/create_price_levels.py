import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from restaurants.models import PriceLevel

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates predefined price levels'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        price_levels = [
            (1, 'Very Cheap', 0, 50),
            (2, 'Cheap', 50, 100),
            (3, 'Moderate', 100, 200),
            (4, 'Expensive', 200, 300),
            (5, 'Very Expensive', 300, 100000)
        ]

        for level, description, min_price, max_price in price_levels:
            price_level, created = PriceLevel.objects.get_or_create(
                level=level,
                defaults={
                    'description': description,
                    'min_price': min_price,
                    'max_price': max_price
                }
            )

            if created:
                logger.info(f'Created PriceLevel {level}: {description}')
            else:
                logger.warning(f'PriceLevel {level} already exists, updating...')

                update_fields = []
                if price_level.description != description:
                    price_level.description = description
                    update_fields.append('description')
                if price_level.min_price != min_price:
                    price_level.min_price = min_price
                    update_fields.append('min_price')
                if price_level.max_price != max_price:
                    price_level.max_price = max_price
                    update_fields.append('max_price')

                if update_fields:
                    price_level.save(update_fields=update_fields)
                    logger.info(f'Updated PriceLevel {level}: {update_fields}')
