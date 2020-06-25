from django.db import models
from django.urls import reverse

CATEGORY_CHOICES = (
    ('P', 'pizza'),
    ('S', 'side'),
    ('D', 'drink'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(max_length=500)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, default="P")
    label = models.CharField(choices=LABEL_CHOICES, max_length=2, default="P")
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def get_add_to_cart_absolute_url(self):
        return reverse("orders:add-to-cart", kwargs={
            'product_id': self.id
        })

    def get_remove_from_cart_absolute_url(self):
        return reverse("orders:remove-from-cart", kwargs={
            'product_id': self.id
        })

    def __str__(self):
        return self.title
