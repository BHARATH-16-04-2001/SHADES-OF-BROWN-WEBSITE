import json
from urllib.parse import parse_qs

import jwt
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from .channels_utils import channel_group_for
from .models import Order


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
    """Admin/chef-facing socket. Every connection joins one shared group and
    gets pushed every new order as it's placed. It also *receives* status
    changes the chef makes ("orderStatus" messages), persists them, and
    fans the update back out to that one customer."""

    GROUP_NAME = "new_orders_backend"

    async def connect(self):
        # TODO: gate this behind staff/chef auth before shipping — right
        # now any connection can both watch every order and change status.
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

    async def receive(self, text_data):
        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Malformed payload — expected JSON.",
            }))
            return

        if payload.get("type") != "orderStatus":
            return  # ignore anything else sent on this connection for now

        order_id = payload.get("order_id")
        new_status = payload.get("status")

        if not order_id or new_status not in Order.Status.values:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "orderStatus requires a valid order_id and status.",
            }))
            return

        order = await self._update_order_status(order_id, new_status)

        if order is None:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": f"Order {order_id} not found.",
            }))
            return

        await self._notify_customer(order)

        # Optional ack back to the chef screen that fired the change.
        await self.send(text_data=json.dumps({
            "type": "orderStatusUpdated",
            "order_id": order.id,
            "status": order.status,
        }))

    async def new_order(self, event):
        await self.send(text_data=json.dumps({
            "type": "new_orders",
            "order": event["order"],
        }))

    @database_sync_to_async
    def _update_order_status(self, order_id, new_status):
        try:
            order = Order.objects.select_related("customer").get(id=order_id)
        except Order.DoesNotExist:
            return None
        order.status = new_status
        order.save(update_fields=["status"])
        return order

    async def _notify_customer(self, order):
        encrypted_phone = order.customer.encrypted_phone
        group_name = channel_group_for(encrypted_phone)
        await self.channel_layer.group_send(
            group_name,
            {
                "type": "order_status_update",  # -> OrderConsumer.order_status_update
                "order_id": order.id,
                "status": order.status,
            },
        )