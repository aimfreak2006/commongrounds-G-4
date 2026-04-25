from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

from accounts.models import Profile


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='products')
    product_image = models.ImageField(
        upload_to='product_images/', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=100000)
    stock = models.IntegerField()
    status = models.CharField(
        choices=[
            ('Available', 'Available'),
            ('On Sale', 'On Sale'),
            ('Out of Stock', 'Out of Stock'),
        ],
        default='Available'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("merchstore:merchstore-detail", kwargs={"id": self.id})


class Transaction(models.Model):
    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        blank=True
    )
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    status = models.CharField(
        choices=[
            ('On cart', 'On cart'),
            ('To Pay', 'To Pay'),
            ('To Ship', 'To Ship'),
            ('To Receive', 'To Receive'),
            ('Delivered', 'Delivered'),
        ]
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer}: {self.amount} {self.product}"
