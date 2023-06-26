import time

from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.FloatField()
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    sold = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProdImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product")


class Newsletter(BaseModel):
    email = models.EmailField()

    def __str__(self) -> str:
        return self.email


class Reviews(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_user")
    review = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.review


class Cart(models.Model):
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Carts'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    dateStamp = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.account.username}: {self.product.name}"

    def total(self):
        return self.quantity * self.product.price