from django.urls import path
from .views import add_to_cart, remove_from_cart

app_name = "orders"

urlpatterns = [
    path('add-to-cart/<product_id>', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<product_id>', remove_from_cart, name="remove-from-cart")
]