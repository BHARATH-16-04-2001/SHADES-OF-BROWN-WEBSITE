from decimal import Decimal

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderItem
from .serializers import CheckoutSerializer


class CheckoutView(APIView):
    serializer_class = CheckoutSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        customer = serializer.validated_data["customer"]
        cart = serializer.validated_data["cart_object"]

        cart_items = cart.items.select_related(
            "food_item"
        ).all()

        # Check food availability
        for cart_item in cart_items:
            if not cart_item.food_item.is_available:
                return Response(
                    {
                        "detail": (
                            f"{cart_item.food_item.name} "
                            "is no longer available."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Calculate subtotal
        subtotal = sum(
            (
                item.food_item.price
                * Decimal(item.quantity)
                for item in cart_items
            ),
            Decimal("0.00"),
        )

        # Discount will be implemented later
        discount = Decimal("0.00")

        total = subtotal - discount

        # Create Order
        order = Order.objects.create(
            customer=customer,
            subtotal=subtotal,
            discount=discount,
            total=total,
        )

        # Create Order Items
        for cart_item in cart_items:
            food_item = cart_item.food_item

            OrderItem.objects.create(
                order=order,
                food_item=food_item,
                food_name=food_item.name,
                quantity=cart_item.quantity,
                unit_price=food_item.price,
                total_price=(
                    food_item.price
                    * Decimal(cart_item.quantity)
                ),
            )

        # Clear the cart after successful checkout
        cart.items.all().delete()

        return Response(
            {
                "message": "Order created successfully.",
                "order": {
                    "id": order.id,
                    "order_number": order.order_number,
                    "customer": order.customer.id,
                    "status": order.status,
                    "subtotal": order.subtotal,
                    "discount": order.discount,
                    "total": order.total,
                },
            },
            status=status.HTTP_201_CREATED,
        )