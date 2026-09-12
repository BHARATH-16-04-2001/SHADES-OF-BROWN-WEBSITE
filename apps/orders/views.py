# from decimal import Decimal

# from django.db import transaction
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .models import Order, OrderItem
# from .serializers import CheckoutSerializer, OrderSerializer


# class CheckoutView(APIView):
#     serializer_class = CheckoutSerializer

#     @transaction.atomic
#     def post(self, request):
#         serializer = self.serializer_class(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         customer = serializer.validated_data["customer"]
#         cart = serializer.validated_data["cart_object"]

#         cart_items = cart.items.select_related(
#             "food_item"
#         ).all()

#         # Check food availability
#         for cart_item in cart_items:
#             if not cart_item.food_item.is_available:
#                 return Response(
#                     {
#                         "detail": (
#                             f"{cart_item.food_item.name} "
#                             "is no longer available."
#                         )
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#         # Calculate subtotal
#         subtotal = sum(
#             (
#                 item.food_item.price
#                 * Decimal(item.quantity)
#                 for item in cart_items
#             ),
#             Decimal("0.00"),
#         )

#         # Discount will be implemented later
#         discount = Decimal("20.00")

#         total = subtotal - discount

#         # Create Order
#         order = Order.objects.create(
#             customer=customer,
#             subtotal=subtotal,
#             discount=discount,
#             total=total,
#         )

#         # Create Order Items
#         for cart_item in cart_items:
#             food_item = cart_item.food_item

#             OrderItem.objects.create(
#                 order=order,
#                 food_item=food_item,
#                 food_name=food_item.name,
#                 quantity=cart_item.quantity,
#                 unit_price=food_item.price,
#                 total_price=(
#                     food_item.price
#                     * Decimal(cart_item.quantity)
#                 ),
#             )

#         # Clear the cart after successful checkout
#         cart.items.all().delete()

#         return Response(
#             {
#                 "message": "Order created successfully.",
#                 "order": {
#                     "id": order.id,
#                     "order_number": order.order_number,
#                     "customer": order.customer.id,
#                     "status": order.status,
#                     "subtotal": order.subtotal,
#                     "discount": order.discount,
#                     "total": order.total,
#                 },
#             },
#             status=status.HTTP_201_CREATED,
#         )


# class OrderListView(APIView):
#     def get(self, request):
#         orders = Order.objects.all().order_by("-created_at")

#         serializer = OrderSerializer(
#             orders,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )



from decimal import Decimal

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from customers.models import Customer

from .models import Order, OrderItem
from .serializers import ActiveOrderSerializer, CheckoutSerializer, ChefOrderSerializer, OrderSerializer, OrderItemSerializer


# class CheckoutView(APIView):
#     serializer_class = CheckoutSerializer

#     @transaction.atomic
#     def post(self, request):
#         serializer = self.serializer_class(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         #  const response = await checkout({
#         # customer_name: form.name,
#         # table_number: form.tableNumber,
#         # phone: form.phone,
#         # items,
#         # subtotal,
#         # cgst,
#         # sgst,
#         # total,

#         # customer = serializer.validated_data["customer"]
#         customer_id = serializer.validated_data["customer"]

#         customer = Customer.objects.get(
#             id=customer_id
#         )
#         cart = serializer.validated_data["cart_object"]

#         cart_items = cart.items.select_related(
#             "food_item"
#         ).all()

#         # Check food availability
#         for cart_item in cart_items:
#             if not cart_item.food_item.is_available:
#                 return Response(
#                     {
#                         "detail": (
#                             f"{cart_item.food_item.name} "
#                             "is no longer available."
#                         )
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#         # Calculate subtotal
#         subtotal = sum(
#             (
#                 item.food_item.price
#                 * Decimal(item.quantity)
#                 for item in cart_items
#             ),
#             Decimal("0.00"),
#         )

#         # Discount - currently zero
#         discount = Decimal("0.00")

#         total = subtotal - discount

#         # Create Order
#         order = Order.objects.create(
#             customer=customer,
#             subtotal=subtotal,
#             discount=discount,
#             total=total,
#         )

#         # Create Order Items
#         for cart_item in cart_items:
#             food_item = cart_item.food_item

#             OrderItem.objects.create(
#                 order=order,
#                 food_item=food_item,
#                 food_name=food_item.name,
#                 quantity=cart_item.quantity,
#                 unit_price=food_item.price,
#                 total_price=(
#                     food_item.price
#                     * Decimal(cart_item.quantity)
#                 ),
#             )

#         # Clear cart
#         cart.items.all().delete()

#         return Response(
#             {
#                 "message": "Order created successfully.",
#                 "order": {
#                     "id": order.id,
#                     "order_number": order.order_number,
#                     "customer": order.customer.id,
#                     "status": order.status,
#                     "subtotal": order.subtotal,
#                     "discount": order.discount,
#                     "total": order.total,
#                     "items": OrderItemSerializer(
#                         order.items.all(),
#                         many=True
#                     ).data,
#                 },
#             },
#             status=status.HTTP_201_CREATED,
#         )

from decimal import Decimal
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .crypto import encrypt_phone
from .auth import generate_order_token
from .broadcasts import broadcast_new_order
from .models import Customer, Order, OrderItem, FoodItem
from .serializers import CheckoutSerializer, ChefOrderSerializer, OrderItemSerializer


class CheckoutView(APIView):
    serializer_class = CheckoutSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # --- customer: find by phone, create if new ---
        phone = data["phone"]
        customer, created = Customer.objects.get_or_create(
            phone=phone,
            defaults={
                "name": data["customer_name"],
                "encrypted_phone": encrypt_phone(phone),
            },
        )
        if not created:
            updates = []
            if customer.name != data["customer_name"]:
                customer.name = data["customer_name"]
                updates.append("name")
            if not customer.encrypted_phone:
                # backfills any customer created before encryption existed
                customer.encrypted_phone = encrypt_phone(phone)
                updates.append("encrypted_phone")
            if updates:
                customer.save(update_fields=updates)

        # --- order ---
        order = Order.objects.create(
            customer=customer,
            table_number=data["table_number"],
            status=Order.Status.PENDING,
            subtotal=data["subtotal"],
            cgst=data["cgst"],
            sgst=data["sgst"],
            total=data["total"],
        )

        # --- order items ---
        order_items = []
        for item in data["items"]:
            unit_price = item["price"]
            order_items.append(
                OrderItem(
                    order=order,
                    food_item=FoodItem.objects.filter(id=item["id"]).first(),
                    food_name=item["name"],
                    quantity=item["quantity"],
                    unit_price=unit_price,
                    total_price=unit_price * item["quantity"],
                )
            )
        OrderItem.objects.bulk_create(order_items)

        # --- token for the customer's own socket + push to every chef screen ---
        token = generate_order_token(customer.encrypted_phone)
        broadcast_new_order(order)

        return Response(
            {
                "message": "Order created successfully.",
                "token": token,
                "customerId": customer.id,
                "customerName": customer.name,
                "customerPhone": customer.phone,
                "encryptedPhone": customer.encrypted_phone,
                "order": ChefOrderSerializer(order).data,
            },
            status=status.HTTP_201_CREATED,
        )

class OrderListView(APIView):

    def get(self, request):
        orders = (
            Order.objects
            .select_related("customer")
            .exclude(
                status__in=[
                    Order.Status.COMPLETED,
                    Order.Status.CANCELLED,
                ]
            )
            .order_by("-created_at")
        )

        serializer = ActiveOrderSerializer(
            orders,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import Customer

from .models import Order
from .serializers import OrderSerializer


class CustomerOrderListView(APIView):

    def get(self, request, customer_id):

        # 1. Verify customer exists
        customer = get_object_or_404(
            Customer,
            id=customer_id
        )

        # 2. Get only this customer's orders
        orders = (
            Order.objects
            .filter(customer=customer)
            .prefetch_related("items")
            .order_by("-created_at")
        )

        # 3. Serialize orders + their items
        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(
            {
                "customerId": customer.id,
                "customerName": customer.name,
                "orders": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
# from .crypto import encrypt_phone
# from .auth import generate_order_token

# class OrderCreateView(APIView):
#     def post(self, request):
#         serializer = OrderSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         encrypted_phone = encrypt_phone(request.data["phone"])
#         order = serializer.save(encrypted_phone=encrypted_phone)

#         token = generate_order_token(encrypted_phone)
#         return Response(
#             {
#                 "order": serializer.data,
#                 "token": token,
#                 "encryptedPhone": encrypted_phone,
#             },
#             status=201,
#         )


from .crypto import encrypt_phone
from .auth import generate_order_token
from .broadcasts import broadcast_new_order

class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        encrypted_phone = encrypt_phone(request.data["phone"])
        customer, _ = Customer.objects.update_or_create(
            phone=request.data["phone"],  # adjust to however you dedupe customers
            defaults={"encrypted_phone": encrypted_phone},
        )
        order = serializer.save(customer=customer)

        token = generate_order_token(encrypted_phone)
        broadcast_new_order(order)

        return Response(
            {"order": serializer.data, "token": token, "encryptedPhone": encrypted_phone},
            status=201,
        )


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .channels_utils import channel_group_for


# def broadcast_order_status(order):
#     channel_layer = get_channel_layer()
#     group_name = channel_group_for(order.encrypted_phone)
#     async_to_sync(channel_layer.group_send)(
#         group_name,
#         {
#             "type": "order_status_update",
#             "order_id": order.id,
#             "status": order.status,
#         },
#     )


# class OrderStatusUpdateView(APIView):
#     def patch(self, request, order_id):
#         order = get_object_or_404(Order, id=order_id)
#         order.status = request.data["status"]
#         order.save(update_fields=["status"])
# 
#         broadcast_order_status(order)
#         return Response(ChefOrderSerializer(order).data)

from .broadcasts import broadcast_order_status
class OrderStatusUpdateView(APIView):

    def patch(self, request):

        order_id = request.data.get("orderId")
        new_status = request.data.get("status")

        if not order_id:
            return Response(
                {"error": "orderId is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not new_status:
            return Response(
                {"error": "status is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = get_object_or_404(
            Order,
            id=order_id,
        )

        order.status = new_status.upper()

        order.save(
            update_fields=["status"]
        )

        # Send updated order through WebSocket
        broadcast_order_status(order)

        return Response(
            ChefOrderSerializer(order).data,
            status=status.HTTP_200_OK,
        )