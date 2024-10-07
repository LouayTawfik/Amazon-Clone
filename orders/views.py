from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, Order, OrderDetail, CartDetail, Coupon
from product.models import Product


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset().prefetch_related(Prefetch('order_detail', queryset=OrderDetail.objects.select_related('product__brand'))).filter(user=self.request.user)
        return queryset

def add_to_cart(request):
    quantity = int(request.POST['quantity'])
    product = Product.objects.get(pk=request.POST['product_id'])

    cart = Cart.objects.get(user=request.user, status='InProgress')
    cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_detail.quantity += quantity
        cart_detail.total = round(cart_detail.quantity * product.price, 2)
        cart_detail.save()
        return redirect(f"/products/{product.slug}")
    cart_detail.quantity = quantity
    cart_detail.total = round(cart_detail.quantity * product.price, 2)
    cart_detail.save()
    return redirect(f"/products/{product.slug}")

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user, status='InProgress')
    cart_detail = CartDetail.objects.select_related('product__brand').filter(cart=cart)
    return render(request, 'orders/checkout.html', {'cart_detail': cart_detail})