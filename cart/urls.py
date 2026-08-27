from django.urls import path

from .views import (
    CartCreateView,
    CartDetailView,
    CartItemCreateView,
    CartItemUpdateView,
    CartItemDeleteView,
)


app_name = "cart"


urlpatterns = [
    path(
        "",
        CartCreateView.as_view(),
        name="cart-create",
    ),
    path(
        "<int:pk>/",
        CartDetailView.as_view(),
        name="cart-detail",
    ),
    path(
        "<int:cart_id>/items/",
        CartItemCreateView.as_view(),
        name="cart-item-create",
    ),

    path(
    "<int:cart_id>/items/<int:item_id>/",
    CartItemUpdateView.as_view(),
    name="cart-item-update",
    ),

    path(
    "<int:cart_id>/items/<int:item_id>/delete/",
    CartItemDeleteView.as_view(),
    name="cart-item-delete",
),
]