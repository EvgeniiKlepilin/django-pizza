from django.db import models
from django.conf import settings
from djangopizza.products.models import Product

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username