from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PriceLevel(models.Model):
    level = models.IntegerField(unique=True, help_text="Price level identifier (e.g., 1, 2, 3, 4, or 5)")
    description = models.CharField(max_length=255, help_text="Description of the price level")
    min_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Minimum price for this level")
    max_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Maximum price for this level")

    def save(self, *args, **kwargs):
        if self.min_price >= self.max_price:
            raise ValueError('Minimum price must be less than maximum price')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.level} - {self.description}'


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price_level = models.ForeignKey(PriceLevel, on_delete=models.PROTECT, help_text="Price level of the restaurant")
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    restaurants = models.ManyToManyField(Restaurant, related_name='categories')

    def __str__(self):
        return self.name


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rating} - {self.review_text[:50]}'


class Image(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='restaurant_images/')
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.restaurant.name} - {self.description}'
