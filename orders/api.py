from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import CartSerializer, OrderListSerializer
from .models import Cart, CartDetail, Order, OrderDetail
from product.models import Product
from django.db.models import Prefetch


class CartDetailCreateAPI(generics.GenericAPIView):
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart, created = Cart.objects.prefetch_related(
            Prefetch('cart_detail', queryset=CartDetail.objects.select_related('product'))).get_or_create(user=user, status='InProgress')

        data = CartSerializer(cart).data
        return Response({'cart': data})
    
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        product = Product.objects.get(pk=request.data['product_id'])
        quantity = int(request.data['quantity'])
        cart = Cart.objects.get(user=user, status='InProgress')
        cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_detail.quantity += quantity
            cart_detail.total = round(cart_detail.quantity * product.price, 2)
            cart_detail.save()
            data = CartSerializer(cart).data
            return Response({'message': 'product updated successfully', 'cart': data})
        cart_detail.quantity = quantity
        cart_detail.total = round(cart_detail.quantity * product.price)
        cart_detail.save()

        data = CartSerializer(cart).data
        return Response({'message': 'product added successfully', 'cart': data})

    def delete(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart_detail = CartDetail.objects.get(pk=request.data['cart_detail_id'])

        cart_detail.delete()

        cart = Cart.objects.prefetch_related(
            Prefetch('cart_detail', queryset=CartDetail.objects.select_related('product'))).get(user=user, status='InProgress')
        data = CartSerializer(cart).data
        return Response({'message': 'product deleted successfully', 'cart': data})


class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderListSerializer
    queryset = Order.objects.select_related('user')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user__username=self.kwargs['username'])
        data = OrderListSerializer(queryset, many=True).data
        return Response(data)
    
    # def get_queryset(self):
    #     queryset = super().get_queryset().filter(user__username=self.kwargs['username'])
    #     return queryset
 

class OrderDetailAPI(generics.RetrieveAPIView):
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()


class CreateOrderAPI(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart = Cart.objects.get(user=user, status='InProgress')
        cart_details = CartDetail.objects.filter(cart=cart)

        # cart -> order
        new_order = Order.objects.create(
            user=user,
            coupon=cart.coupon,
            total_after_coupon=cart.total_after_coupon
        )

        # cart_detail  --> order_detail -----> loop
        for cart_detail in cart_details:
            OrderDetail.objects.create(
                order=new_order,
                product=cart_detail.product,
                quantity=cart_detail.quantity,
                price=cart_detail.product.price,
                total=round(int(cart_detail.quantity) * cart_detail.product.price, 2)
            )

        cart.status = 'Completed'
        cart.save()
        return Response({'message', 'Order Created Successfully'})


class ApplyCouponAPI(generics.GenericAPIView):
    pass
