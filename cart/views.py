from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import Customer
from apps.menu.models import FoodItem

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartCreateView(CreateAPIView):
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get("customer")

        if not customer_id:
            return Response(
                {
                    "customer": [
                        "Customer is required."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        customer = get_object_or_404(
            Customer,
            id=customer_id,
        )

        cart = Cart.objects.create(
            customer=customer,
        )

        serializer = self.get_serializer(cart)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CartDetailView(RetrieveAPIView):
    queryset = Cart.objects.prefetch_related(
        "items__food_item"
    )
    serializer_class = CartSerializer


class CartItemCreateView(APIView):

    def post(self, request, cart_id):
        cart = get_object_or_404(
            Cart,
            id=cart_id,
        )

        food_item_id = request.data.get(
            "food_item"
        )

        quantity = request.data.get(
            "quantity",
            1,
        )

        if not food_item_id:
            return Response(
                {
                    "food_item": [
                        "Food item is required."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        food_item = get_object_or_404(
            FoodItem,
            id=food_item_id,
            is_available=True,
        )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {
                    "quantity": [
                        "Quantity must be a valid number."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:
            return Response(
                {
                    "quantity": [
                        "Quantity must be at least 1."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            food_item=food_item,
            defaults={
                "quantity": quantity,
            },
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

        serializer = CartItemSerializer(
            cart_item
        )

        return Response(
            serializer.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )

class CartItemUpdateView(APIView):

    def patch(self, request, cart_id, item_id):
        cart = get_object_or_404(
            Cart,
            id=cart_id,
        )

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart=cart,
        )

        quantity = request.data.get("quantity")

        if quantity is None:
            return Response(
                {
                    "quantity": [
                        "Quantity is required."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {
                    "quantity": [
                        "Quantity must be a valid number."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:
            return Response(
                {
                    "quantity": [
                        "Quantity must be at least 1."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item.quantity = quantity
        cart_item.save(
            update_fields=[
                "quantity",
                "updated_at",
            ]
        )

        serializer = CartItemSerializer(
            cart_item
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class CartItemDeleteView(APIView):

    def delete(self, request, cart_id, item_id):
        cart = get_object_or_404(
            Cart,
            id=cart_id,
        )

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart=cart,
        )

        cart_item.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    

# class CartItemDeleteView(APIView):

#     def delete(self, request, cart_id, item_id):
#         cart = get_object_or_404(
#             Cart,
#             id=cart_id,
#         )

#         cart_item = get_object_or_404(
#             CartItem,
#             id=item_id,
#             cart=cart,
#         )

#         cart_item.delete()

#         return Response(
#             {
#                 "detail": "Cart item removed successfully."
#             },
#             status=status.HTTP_200_OK,
        # )