# restaurants/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    cuisine_type = models.CharField(max_length=100, default="Unknown")
    place_id = models.CharField(max_length=255, unique=True)  # Enforce uniqueness
    formatted_phone_number = models.CharField(max_length=20, blank=True, null=True)  # Renamed field

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant_detail', args=[self.place_id])

    def clean(self):
        # Ensure the latitude and longitude are within valid ranges
        if not (-90 <= self.latitude <= 90):
            raise ValidationError({'latitude': 'Latitude must be between -90 and 90.'})
        if not (-180 <= self.longitude <= 180):
            raise ValidationError({'longitude': 'Longitude must be between -180 and 180.'})
    
    def save(self, *args, **kwargs):
        # Additional validation checks before saving
        self.clean()  # Ensures that the clean method is called
        super(Restaurant, self).save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    place_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255, default='Unknown')  # Assign default
    address = models.CharField(max_length=255, blank=True, null=True, default='No address available')
    rating = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place_id')  # Prevent duplicate favorites

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def clean(self):
        # Ensure rating is within valid bounds if provided
        if self.rating and not (0 <= self.rating <= 5):
            raise ValidationError({'rating': 'Rating must be between 0 and 5.'})

    def save(self, *args, **kwargs):
        # Call clean method before saving to validate data
        self.clean()
        super(Favorite, self).save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # Rating out of 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Newest reviews first

    def __str__(self):
        return f"Review by {self
