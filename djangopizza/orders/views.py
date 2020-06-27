from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import View
from django.utils import timezone
from .models import Order, OrderItem, ShippingAddress
from .forms import CheckoutForm
from djangopizza.products.models import Product


class CheckoutView(View):

    def get(self, *args, **kwargs):
        first_name = self.request.user.first_name
        last_name = self.request.user.last_name
        email = self.request.user.email

        shipping_address_qs = ShippingAddress.objects.filter(
            user=self.request.user,
        )

        if shipping_address_qs.exists():
            shipping_address = shipping_address_qs[0]
            form = CheckoutForm(initial={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'street_address': shipping_address.street_address,
                'apartment_address': shipping_address.apartment_address,
                'country': shipping_address.country,
                'zip_code': shipping_address.zip_code,
            })
        else:
            form = CheckoutForm(initial={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
        try:
            order = Order.objects.get(
                user=self.request.user,
                is_ordered=False
            )
            if not order.items.exists() or order.get_total_price() == 0:
                messages.warning(self.request, "You do not have anything to checkout.")
                return redirect("products:product-list")
            context = {
                'form': form,
                'order': order
            }
            return render(self.request, 'orders/checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("products:product-list")        

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(
                user=self.request.user,
                is_ordered=False
            )
            if form.is_valid():
                user = self.request.user
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.save()

                shipping_address, created = ShippingAddress.objects.get_or_create(
                    user=user,
                    street_address = form.cleaned_data.get('street_address'),
                    apartment_address = form.cleaned_data.get('apartment_address'),
                    country = form.cleaned_data.get('country'),
                    zip_code = form.cleaned_data.get('zip_code'),
                )
                if created:
                    shipping_address.save()
                order.shipping_address = shipping_address
                order.ordered_date = timezone.now()
                order.is_ordered = True
                order.save()
                messages.success(self.request, "You have successfully placed an order!")
                return redirect("products:product-list")
            messages.warning(self.request, "Failed to process checkout form")
            return redirect("orders:checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("products:product-list")
        

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
            messages.warning(self.request, "You do not have an active order.")
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