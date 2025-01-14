from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, Order, OrderDetail, CartDetail, Coupon
from product.models import Product
from django.shortcuts import get_object_or_404
from settings.models import DeliveryFee
import datetime



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

def remove_from_cart(request, id):
    cart_detail = CartDetail.objects.get(pk=id)
    cart_detail.delete()
    return redirect(f"/products/")

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user, status='InProgress')
    cart_detail = CartDetail.objects.select_related('product__brand').filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee

    if request.method == 'POST':
        coupon = get_object_or_404(Coupon, code=request.POST.get('coupon_code'))

        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()

            if coupon.start_date <= today_date <= coupon.end_date:
                coupon_value = cart.cart_total() * coupon.discount / 100
                cart_total = cart.cart_total() - coupon_value

                coupon.quantity -= 1
                coupon.save()

                cart.coupon = coupon
                cart.total_after_coupon = cart_total
                cart.save()

                total = delivery_fee + cart_total

                return render(request, 'orders/checkout.html', {
                    'cart_detail': cart_detail,
                    'sub_total': cart_total,
                    'cart_total': total,
                    'coupon': coupon_value,
                    'delivery_fee': delivery_fee
                })
    sub_total = cart.cart_total()
    total = delivery_fee + sub_total
    coupon = 0


    return render(request, 'orders/checkout.html', {
        'cart_detail': cart_detail,
        'sub_total': sub_total,
        'cart_total': total,
        'coupon': coupon,
        'delivery_fee': delivery_fee
        })