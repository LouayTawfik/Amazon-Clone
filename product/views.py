from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Brand, ProductImages, Review

class ProductList(ListView):
    model = Product


class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.get_object())
        return context
