from django import template
from ..models import Order
import requests

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(
            user=user,
            is_ordered=False
        )
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def to_euro(usd_amount):
    response = requests.get('https://api.exchangeratesapi.io/latest?symbols=USD')
    data = response.json()
    return round(usd_amount / data['rates']['USD'], 1)