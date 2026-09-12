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


class ChefOrderSerializer(serializers.ModelSerializer):
    orderId = serializers.IntegerField(source="id", read_only=True)
    customerName = serializers.CharField(
        source="customer.name",
        read_only=True
    )
    customerId = serializers.IntegerField(
        source="customer.id",
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "orderId",
            "status",
            "customerName",
            "customerId",
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

class ActiveOrderSerializer(serializers.ModelSerializer):
    orderId = serializers.IntegerField(source="id", read_only=True)
    customerId = serializers.IntegerField(source="customer.id", read_only=True)
    customerName = serializers.CharField(source="customer.name", read_only=True)


    class Meta:
        model = Order
        fields = [
            "orderId",
            "status",
            "customerName",
            "customerId",
        ]