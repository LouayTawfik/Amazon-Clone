from django.urls import path
from .views import BrandList, ProductList, ProductDetail

urlpatterns = [
    path('', ProductList.as_view()),
    path('<slug:slug>', ProductDetail.as_view()),
    path('brands/', BrandList.as_view())
]
