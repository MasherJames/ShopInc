from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True)
    price = models.IntegerField(default=0)
    added_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    image_url = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
