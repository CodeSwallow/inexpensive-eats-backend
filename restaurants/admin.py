from django.contrib import admin

from restaurants.models import (
    Restaurant,
    Category,
    PriceLevel,
    Review,
    Image
)


@admin.register(PriceLevel)
class PriceLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'description', 'min_price', 'max_price')
    list_filter = ('level',)
    search_fields = ('description',)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'price_level', 'rating', 'created_at')
    list_filter = ('price_level', 'rating', 'created_at')
    search_fields = ('name', 'address')
    raw_id_fields = ('price_level',)
    date_hierarchy = 'created_at'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('restaurant__name', 'review_text')
    date_hierarchy = 'created_at'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('restaurant__name', 'description')
    date_hierarchy = 'created_at'

