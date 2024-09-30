from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db.models import Prefetch
from django.views.generic import ListView
from .models import Cart, Order, OrderDetail, CartDetail, Coupon


class OrderListView(ListView):
    model = Order
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset().prefetch_related(Prefetch('order_detail', queryset=OrderDetail.objects.select_related('product__brand'))).filter(user=self.request.user)
        return queryset


def checkout(request):
    cart = Cart.objects.get(user=request.user, status='InProgress')
    cart_detail = CartDetail.objects.select_related('product__brand').filter(cart=cart)
    return render(request, 'orders/checkout.html', {'cart_detail': cart_detail})