from django.db import models
from django.utils.text import slugify
from django.core.files.storage import default_storage

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class, e.g. fa-car", blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Car(models.Model):
    FUEL_CHOICES = (
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    )
    TRANSMISSION_CHOICES = (
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
    )

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cars')
    model_name = models.CharField(max_length=150)
    year = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_length=10, max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    seats = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField(help_text="Mileage in km/l or km range")
    air_conditioning = models.BooleanField(default=True)
    gps = models.BooleanField(default=True)
    bluetooth = models.BooleanField(default=True)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    main_image = models.ImageField(upload_to='cars/')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand.name} {self.model_name} ({self.year})"

    @property
    def name(self):
        return f"{self.brand.name} {self.model_name}"

    @property
    def image_url(self):
        placeholder = 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&q=80&w=1200'
        if self.main_image and default_storage.exists(self.main_image.name):
            return self.main_image.url
        return placeholder

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/gallery/')

    @property
    def image_url(self):
        if self.image and default_storage.exists(self.image.name):
            return self.image.url
        return self.car.image_url

    def __str__(self):
        return f"Gallery Image for {self.car}"
