from django.urls import path,include
from .base import HealthCheckView
from apps import *

urlpatterns = [
    path(
        "health/",
        HealthCheckView.as_view(),
        name="api-health",
    ),
    path(
        "menu/",
        include("apps.menu.urls"),
    ),

    path(
        "customers/",
        include("customers.urls"),
    ),
    path(
    "cart/",
    include("cart.urls"),
    ),

    path(
    "orders/",
    include("apps.orders.urls"),
    ),

    path(
        "cafe-tables/",
        include(
            "apps.cafe_tables.urls",
            namespace="cafe_tables",
        ),
    )
]