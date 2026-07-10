from django.db import models
from django.conf import settings
from rental.models.car import Car

class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    cars = models.ManyToManyField(Car, related_name='wishlists', blank=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"
