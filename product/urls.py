from django.urls import path
from .views import BrandDetail, BrandList, ProductList, ProductDetail
from .api import product_detail_api, product_list_api

urlpatterns = [
    path('', ProductList.as_view()),
    path('<slug:slug>', ProductDetail.as_view()),
    path('brands/', BrandList.as_view()),
    path('brands/<slug:slug>', BrandDetail.as_view()),

    # api
    path('api/list', product_list_api),
    path('api/detail/<int:product_id>', product_detail_api)
]
