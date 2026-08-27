from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "customer__name",
        "customer__phone",
    )

    ordering = (
        "-updated_at",
    )

    inlines = [
        CartItemInline,
    ]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "food_item",
        "quantity",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "food_item__name",
        "cart__customer__name",
        "cart__customer__phone",
    )