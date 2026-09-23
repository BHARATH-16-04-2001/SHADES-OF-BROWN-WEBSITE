from django.urls import path

from .views import CheckoutView, OrderListView, CustomerOrderListView
from .consumers import NewOrderConsumer
from .views import CustomerOrderPhoneListView

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

       path(
        "customers/<int:customer_id>/orders/",
        CustomerOrderListView.as_view(),
        name="customer-orders",
    ),
       
        path(
        "ws/orders/",           
        NewOrderConsumer.as_asgi(),
    ),
    
        path(
            "customer/phone/<str:phone_no>/",
            CustomerOrderPhoneListView.as_view(),
            name="customer-orders-by-phone",
        ),

]