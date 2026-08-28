from django.urls import path

from .views import CheckoutView, OrderListView


app_name = "orders"


urlpatterns = [
    path(
        "checkout/",
        CheckoutView.as_view(),
        name="checkout",
    ),

     path(
        "",
        OrderListView.as_view(),
        name="order-list",
    ),
]