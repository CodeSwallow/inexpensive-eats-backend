from django.core.management.base import BaseCommand, CommandError

from restaurants.models import Restaurant


class Command(BaseCommand):
    help = 'Scrapes restaurants from Google Places API'

    def handle(self, *args, **options):
        Restaurant.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all restaurants'))
