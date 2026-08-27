from rest_framework import serializers

from cart.models import Cart
from customers.models import Customer


class CheckoutSerializer(serializers.Serializer):
    customer = serializers.IntegerField(
        required=True
    )

    cart = serializers.IntegerField(
        required=True
    )

    def validate_customer(self, value):
        if not Customer.objects.filter(
            id=value
        ).exists():
            raise serializers.ValidationError(
                "Customer does not exist."
            )

        return value

    def validate_cart(self, value):
        if not Cart.objects.filter(
            id=value
        ).exists():
            raise serializers.ValidationError(
                "Cart does not exist."
            )

        return value

    def validate(self, attrs):
        customer_id = attrs["customer"]
        cart_id = attrs["cart"]

        cart = Cart.objects.filter(
            id=cart_id,
            customer_id=customer_id,
        ).first()

        if not cart:
            raise serializers.ValidationError(
                "This cart does not belong to this customer."
            )

        if not cart.items.exists():
            raise serializers.ValidationError(
                "Cannot checkout an empty cart."
            )

        attrs["cart_object"] = cart

        return attrs