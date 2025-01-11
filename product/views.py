from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Product, Brand, ProductImages, Review
from django.db.models.aggregates import Count
from .tasks import send_emails

class ProductList(ListView):
    model = Product
    paginate_by = 30

    def get_queryset(self) -> QuerySet[Any]:
        # send_emails.delay()
        return super().get_queryset().prefetch_related('review_product')
        # return super().get_queryset().order_by('id').prefetch_related('review_product')

class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.get_object())
        context['related_products'] = Product.objects.filter(brand=self.get_object().brand)
        return context
    

class BrandList(ListView):
    model = Brand  # context: object_list, model_list
    queryset = Brand.objects.annotate(product_count=Count('product_brand'))


class BrandDetail(ListView):
    model = Product
    template_name = 'product/brand_detail.html'
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:  # override query
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        return super().get_queryset().filter(brand=brand)
    
    # retrieve new data: template
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['brand'] = Brand.objects.filter(slug=self.kwargs['slug']).annotate(product_count=Count('product_brand'))[0]
        return context
    

# def brand_list(request):
#     brands = Brand.objects.all()  # queryset: query db
#     context = {'data': brands}
#     return render(request, 'brands.html', context)

def add_review(request, slug):
    product = Product.objects.get(slug=slug)

    rate = request.POST.get('rate')
    review = request.POST.get('review')

    Review.objects.create(
        product=product,
        rate=rate,
        review=review,
        user=request.user
    )

    return redirect(f'/products/{product.slug}')

