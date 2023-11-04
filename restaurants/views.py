from django.shortcuts import render
from django.views import View

from restaurants.models import Restaurant


class HomePageView(View):
    template_name = 'restaurants/home.html'

    def get(self, request, *args, **kwargs):
        newest_restaurants = Restaurant.objects.order_by('-created_at')[:5]
        popular_restaurants = Restaurant.objects.order_by('-rating')[:5]

        return render(request, self.template_name, {
            'newest_restaurants': newest_restaurants,
            'popular_restaurants': popular_restaurants
        })
