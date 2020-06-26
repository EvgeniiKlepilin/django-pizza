from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Order, OrderItem
from djangopizza.products.models import Product


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user,
                is_ordered=False
            )
            context = {
                'object': order
            }
            return render(self.request, 'orders/summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect("products:product-list")
        


@login_required
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
    return redirect(request.META.get('HTTP_REFERER', "orders:summary"))


@login_required
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
                order_item.save()
                messages.info(request, f"{product.title} quantity has been updated.")
        else:
            messages.info(request, f"{product.title} was not in your cart.")
    else:
        messages.info(request, "You do not have an active order.")
    return redirect(request.META.get('HTTP_REFERER', "orders:summary"))