from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "food_name",
        "unit_price",
        "total_price",
        "created_at",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "customer",
        "status",
        "subtotal",
        "discount",
        "total",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "customer__name",
        "customer__phone",
    )

    readonly_fields = (
        "order_number",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "food_name",
        "quantity",
        "unit_price",
        "total_price",
        "created_at",
    )

    search_fields = (
        "order__order_number",
        "food_name",
        "order__customer__name",
        "order__customer__phone",
    )

    readonly_fields = (
        "food_name",
        "unit_price",
        "total_price",
        "created_at",
    )