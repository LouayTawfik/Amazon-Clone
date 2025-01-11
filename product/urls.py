from django.urls import path
from .views import BrandDetail, BrandList, ProductList, ProductDetail, add_review
from .api import ProductListAPI, ProductDetailAPI, BrandListAPI, BrandDetailAPI

app_name = 'product'

urlpatterns = [
    path('', ProductList.as_view()),
    path('<slug:slug>', ProductDetail.as_view()),
    path('brands/', BrandList.as_view()),
    path('brands/<slug:slug>', BrandDetail.as_view()),
    path('<slug:slug>/add-review', add_review, name='add-review'),

    # api
    path('api/list', ProductListAPI.as_view()),
    path('api/detail/<int:pk>', ProductDetailAPI.as_view()),

    path('brands/api/list', BrandListAPI.as_view()),
    path('brands/api/detail/<int:pk>', BrandDetailAPI.as_view())
]
