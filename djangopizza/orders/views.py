from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem
from djangopizza.products.models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        is_ordered=False
    )
    order_qs = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__id=product_id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{product.title} quantity has been updated.")
        else:
            order.items.add(order_item)
            messages.info(request, f"{product.title} has been added to your cart.")
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, f"{product.title} has been added to your cart.")
    return redirect("products:product-list")

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order_qs = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__id=product_id).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                is_ordered=False
            )[0]
            if order_item.quantity == 1:
                order.items.remove(order_item)
                messages.info(request, f"{product.title} has been removed from your cart.")
            else:
                order_item.quantity -= 1
                messages.info(request, f"{product.title} quantity has been updated.")
        else:
            messages.info(request, f"{product.title} was not in your cart.")
    else:
        messages.info(request, "You do not have an active order.")
    return redirect("products:product-list")