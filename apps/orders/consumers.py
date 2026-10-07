import json
from urllib.parse import parse_qs

import jwt
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from .channels_utils import channel_group_for
from .models import Order

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import ChefOrderSerializer


class OrderConsumer(AsyncWebsocketConsumer):
    """Customer-facing socket — one connection per order, scoped to that
    customer's encrypted phone number via the JWT issued at checkout."""

    async def connect(self):
        query_string = self.scope["query_string"].decode()
        token = parse_qs(query_string).get("token", [None])[0]

        if not token:
            await self.close(code=4401)
            return

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            await self.close(code=4401)
            return
        except jwt.InvalidTokenError:
            await self.close(code=4403)
            return

        encrypted_phone = payload.get("ep")
        if not encrypted_phone:
            await self.close(code=4403)
            return

        self.group_name = channel_group_for(encrypted_phone)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass  # customer screens only listen

    async def order_status_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "order_status_update",
            "order_id": event["order_id"],
            "status": event["status"],
        }))

class NewOrderConsumer(AsyncWebsocketConsumer):

    GROUP_NAME = "new_orders_backend"

    async def connect(self):
        print(
            "ADMIN CONNECT:",
            self.channel_name
        )

        await self.channel_layer.group_add(
            self.GROUP_NAME,
            self.channel_name
        )

        await self.accept()

        print(
            "ADMIN CONNECTED:",
            self.channel_name
        )

    async def disconnect(self, close_code):
        print(
            "ADMIN DISCONNECT:",
            self.channel_name,
            "code:",
            close_code
        )

        await self.channel_layer.group_discard(
            self.GROUP_NAME,
            self.channel_name
        )

    async def receive(self, text_data):

        print(
            "ADMIN MESSAGE:",
            text_data
        )

        try:
            payload = json.loads(text_data)

        except json.JSONDecodeError as e:

            print(
                "JSON ERROR:",
                str(e)
            )

            return

        if payload.get("type") != "orderStatus":
            return

        order_id = payload.get("order_id")
        new_status = payload.get("status")

        print(
            "STATUS REQUEST:",
            order_id,
            new_status
        )

        if (
            not order_id
            or new_status not in Order.Status.values
        ):
            await self.send(
                text_data=json.dumps({
                    "type": "error",
                    "message": "Invalid order status",
                })
            )
            return

        try:

            order = await self._update_order_status(
                order_id,
                new_status
            )

            if order is None:

                await self.send(
                    text_data=json.dumps({
                        "type": "error",
                        "message": (
                            f"Order {order_id} "
                            "not found."
                        ),
                    })
                )

                return

            print(
                "ORDER UPDATED:",
                order.id,
                order.status
            )

            # ---------------------------------
            # Notify customer
            # ---------------------------------

            await self._notify_customer(order)

            print(
                "CUSTOMER NOTIFIED"
            )

            # ---------------------------------
            # Serialize order safely
            # ---------------------------------

            serialized_order = (
                await self._serialize_order(order)
            )

            print(
                "SERIALIZED ORDER:",
                serialized_order
            )

            # ---------------------------------
            # Broadcast to ALL admins
            # ---------------------------------

            await self.channel_layer.group_send(
                self.GROUP_NAME,
                {
                    "type":
                        "order_status_update",

                    "order":
                        serialized_order,
                },
            )

            print(
                "ADMIN BROADCAST SENT"
            )

        except Exception as e:

            import traceback

            print(
                "🔥 WEBSOCKET ERROR:",
                repr(e)
            )

            traceback.print_exc()

            await self.send(
                text_data=json.dumps({
                    "type": "error",
                    "message": str(e),
                })
            )

    async def new_order(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "new_order",
                "order": event["order"],
            })
        )

    async def order_status_update(
        self,
        event
    ):

        print(
            "📢 SENDING TO ADMIN:",
            self.channel_name,
            event["order"]
        )

        await self.send(
            text_data=json.dumps({
                "type":
                    "order_status_update",

                "order":
                    event["order"],
            })
        )

    @database_sync_to_async
    def _update_order_status(
        self,
        order_id,
        new_status
    ):

        try:

            order = (
                Order.objects
                .select_related("customer")
                .get(id=order_id)
            )

        except Order.DoesNotExist:

            return None

        order.status = new_status

        order.save(
            update_fields=["status"]
        )

        return order

    @database_sync_to_async
    def _serialize_order(self, order):

        return ChefOrderSerializer(
            order
        ).data

    async def _notify_customer(self, order):

        encrypted_phone = (
            order.customer.encrypted_phone
        )

        group_name = channel_group_for(
            encrypted_phone
        )

        await self.channel_layer.group_send(
            group_name,
            {
                "type": "order_status_update",

                "order_id": order.id,

                "status": order.status,
            },
        )