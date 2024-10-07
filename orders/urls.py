from django.urls import path
from .views import OrderListView, checkout, add_to_cart, remove_from_cart

urlpatterns = [
    path('', OrderListView.as_view()),
    path('checkout', checkout),
    path('add-to-cart', add_to_cart, name='add_to_cart'),
    path('<int:id>/remove-from-cart', remove_from_cart)
]
