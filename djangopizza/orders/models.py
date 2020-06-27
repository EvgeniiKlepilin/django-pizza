from django.db import models
from django.conf import settings
from djangopizza.products.models import Product
from django_countries.fields import CountryField

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return str(self.quantity) + " of " + self.product.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    delivery = models.ForeignKey(
        'Delivery',
        on_delete=models.SET_NULL,
        default=1,
        blank=True,
        null=True,
    )
    shipping_address = models.ForeignKey(
        'ShippingAddress',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_total_price()
        return total + self.delivery.cost

    def __str__(self):
        return self.user.username


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Delivery(models.Model):
    cost = models.FloatField()
    country = CountryField(multiple=False, blank=True, null=True, unique=True)

    def __str__(self):
        if not self.country:
            return "Generic Delivery"
        else:
            return f"Delivery to {self.country}"