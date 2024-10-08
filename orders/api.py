from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import CartSerializer
from .models import Cart, CartDetail
from product.models import Product
from django.db.models import Prefetch


class CartDetailCreateAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart, created = Cart.objects.prefetch_related(Prefetch('cart_detail', queryset=CartDetail.objects.select_related('product'))).get_or_create(user=user)

        data = CartSerializer(cart).data
        return Response({'cart': data})
        