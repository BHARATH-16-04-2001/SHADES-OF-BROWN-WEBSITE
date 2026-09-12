# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r"ws/orders/$", consumers.OrderConsumer.as_asgi()),
#     re_path(r"ws/new-orders/$", consumers.NewOrderConsumer.as_asgi()),
# ]
# orders/routing.py

from django.urls import path

from .consumers import NewOrderConsumer


websocket_urlpatterns = [
    path(
        "ws/orders/",
        NewOrderConsumer.as_asgi(),
    ),
]