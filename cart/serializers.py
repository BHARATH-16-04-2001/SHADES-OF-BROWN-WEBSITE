from decimal import Decimal
from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.CharField(
        source="food_item.name",
        read_only=True,
    )

    unit_price = serializers.DecimalField(
        source="food_item.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "food_item",
            "food_item_name",
            "quantity",
            "unit_price",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "food_item_name",
            "unit_price",
            "total_price",
            "created_at",
            "updated_at",
        ]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Quantity must be at least 1."
            )

        return value

    def get_total_price(self, obj):
        return (
            obj.food_item.price
            * Decimal(obj.quantity)
        )


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "customer",
            "items",
            "subtotal",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "items",
            "subtotal",
            "created_at",
            "updated_at",
        ]

    def get_subtotal(self, obj):
        return sum(
            (
                item.food_item.price
                * Decimal(item.quantity)
                for item in obj.items.all()
            ),
            Decimal("0.00"),
        )