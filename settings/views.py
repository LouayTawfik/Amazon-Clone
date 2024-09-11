from django.shortcuts import render
from product.models import Product, Brand, Review
from django.db.models import Count

def home(request):
    brands = Brand.objects.all().annotate(product_count=Count('product_brand'))
    sale_products = Product.objects.prefetch_related('review_product').filter(flag='Sale')[:10]
    feature_products = Product.objects.prefetch_related('review_product').filter(flag='Feature')[:6]
    new_products = Product.objects.prefetch_related('review_product').filter(flag='New')[:10]
    reviews = Review.objects.select_related('user').all()[:5]
    return render(request, 'settings/home.html', {
        'brands': brands,
        'sale_products': sale_products,
        'feature_products': feature_products,
        'new_products': new_products,
        'reviews': reviews
    })
