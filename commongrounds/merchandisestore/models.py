from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeingKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='products'
    )
    description = models.TextField()
    price = models.DecimalField(decimal_places=2)

    class Meta:
        ordering = ['name']
