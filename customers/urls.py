from django.urls import path

from .views import (
    CustomerCreateView,
    CustomerDetailView,
)


app_name = "customers"


urlpatterns = [
    path(
        "",
        CustomerCreateView.as_view(),
        name="customer-create",
    ),
    path(
        "<int:pk>/",
        CustomerDetailView.as_view(),
        name="customer-detail",
    ),
]