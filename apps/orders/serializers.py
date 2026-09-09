# from rest_framework import serializers
# from cart.models import Cart
# from customers.models import Customer
# from .models import Order


# class CheckoutSerializer(serializers.Serializer):
#     customer = serializers.IntegerField(
#         required=True
#     )

#     cart = serializers.IntegerField(
#         required=True
#     )

#     def validate_customer(self, value):
#         if not Customer.objects.filter(
#             id=value
#         ).exists():
#             raise serializers.ValidationError(
#                 "Customer does not exist."
#             )

#         return value

#     def validate_cart(self, value):
#         if not Cart.objects.filter(
#             id=value
#         ).exists():
#             raise serializers.ValidationError(
#                 "Cart does not exist."
#             )

#         return value

#     def validate(self, attrs):
#         customer_id = attrs["customer"]
#         cart_id = attrs["cart"]

#         cart = Cart.objects.filter(
#             id=cart_id,
#             customer_id=customer_id,
#         ).first()

#         if not cart:
#             raise serializers.ValidationError(
#                 "This cart does not belong to this customer."
#             )

#         if not cart.items.exists():
#             raise serializers.ValidationError(
#                 "Cannot checkout an empty cart."
#             )

#         attrs["cart_object"] = cart

#         return attrs


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = [
#             "id",
#             "order_number",
#             "customer",
#             "status",
#             "subtotal",
#             "discount",
#             "total",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = [
#             "id",
#             "order_number",
#             "customer",
#             "status",
#             "subtotal",
#             "discount",
#             "total",
#             "created_at",
#             "updated_at",
#         ]



from django.db import models
from rest_framework import serializers

from cart.models import Cart
from customers.models import Customer
from .models import Order, OrderItem


# class CheckoutSerializer(serializers.Serializer):
#     customer = serializers.IntegerField(
#         required=True
#     )

#     cart = serializers.IntegerField(
#         required=True
#     )

#     def validate_customer(self, value):
#         if not Customer.objects.filter(
#             id=value
#         ).exists():
#             raise serializers.ValidationError(
#                 "Customer does not exist."
#             )

#         return value

#     def validate_cart(self, value):
#         if not Cart.objects.filter(
#             id=value
#         ).exists():
#             raise serializers.ValidationError(
#                 "Cart does not exist."
#             )

#         return value

#     def validate(self, attrs):
#         customer_id = attrs["customer"]
#         cart_id = attrs["cart"]

#         cart = Cart.objects.filter(
#             id=cart_id,
#             customer_id=customer_id,
#         ).first()

#         if not cart:
#             raise serializers.ValidationError(
#                 "This cart does not belong to this customer."
#             )

#         if not cart.items.exists():
#             raise serializers.ValidationError(
#                 "Cannot checkout an empty cart."
#             )

#         attrs["cart_object"] = cart

#         return attrs

class CheckoutItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)


class CheckoutSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255)
    table_number = serializers.CharField(max_length=50)
    phone = serializers.RegexField(regex=r"^\d{10}$")
    items = CheckoutItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    cgst = serializers.DecimalField(max_digits=10, decimal_places=2)
    sgst = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


class ChefOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["food_name", "quantity", "unit_price", "total_price"]


class ChefOrderSerializer(serializers.ModelSerializer):
    items = ChefOrderItemSerializer(many=True, read_only=True)
    # exposed for reference only — opaque to the chef, never the raw phone
    encrypted_phone = serializers.CharField(source="customer.encrypted_phone", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "customer_name", "table_number", "status",
            "subtotal", "cgst", "sgst", "total", "created_at",
            "items", "encrypted_phone",
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "food_item",
            "food_name",
            "quantity",
            "unit_price",
            "total_price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer",
            "status",
            "subtotal",
            "discount",
            "total",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "order_number",
            "customer",
            "status",
            "subtotal",
            "discount",
            "total",
            "items",
            "created_at",
            "updated_at",
        ]

# class ChefOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = [
#             "id", "customer_name", "table_number", "items",
#             "status", "total", "placed_at",
#             "encrypted_phone",  # opaque to the chef — used only for reference
#         ]
        # raw `phone` is deliberately not in this list