from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Customer, Order


class CheckoutView(APIView):

    def post(self, request):

        customer_name = request.data.get("customer_name")
        phone = request.data.get("phone")
        table_number = request.data.get("table_number")
        items = request.data.get("items", [])

        subtotal = request.data.get("subtotal")
        cgst = request.data.get("cgst")
        sgst = request.data.get("sgst")
        total = request.data.get("total")

        # 1. Find customer using phone
        customer = Customer.objects.filter(phone=phone).first()

        # 2. If customer doesn't exist, create customer
        if not customer:
            customer = Customer.objects.create(
                name=customer_name,
                phone=phone
            )

        # 3. Generate Order ID
        order_id = f"ORD-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        # 4. Create order
        order = Order.objects.create(
            order_id=order_id,
            customer=customer,
            table_number=table_number,
            items=items,
            subtotal=subtotal,
            cgst=cgst,
            sgst=sgst,
            total=total
        )

        return Response(
            {
                "success": True,
                "message": "Order created successfully",
                "order_id": order.order_id,
                "customer_id": customer.id,
                "created_at": order.created_at
            },
            status=status.HTTP_201_CREATED
        )