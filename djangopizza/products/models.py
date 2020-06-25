from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.title
