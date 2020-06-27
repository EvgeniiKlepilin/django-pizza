from django.urls import path
from .views import add_to_cart, remove_from_cart, OrderSummaryView, CheckoutView, OrderHistoryView

app_name = "orders"

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('order-summary/', OrderSummaryView.as_view(), name="summary"),
    path('order-history/', OrderHistoryView.as_view(), name="history"),
    path('add-to-cart/<product_id>', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<product_id>', remove_from_cart, name="remove-from-cart")
]