from django.urls import path
from .views import OrderListView, checkout

urlpatterns = [
    path('', OrderListView.as_view()),
    path('checkout', checkout),
]
