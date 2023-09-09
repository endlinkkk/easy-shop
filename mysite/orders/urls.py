from django.urls import path
from .views import BasketView, OrderView, OrderIdView

urlpatterns = [
    path("basket", BasketView.as_view(), name="basket"),
    path("orders", OrderView.as_view(), name="orders"),
    path("order/<int:id>", OrderIdView.as_view(), name="orders-id"),
]
