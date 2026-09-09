from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .channels_utils import channel_group_for
from .serializers import ChefOrderSerializer


def broadcast_new_order(order):
    """Pushed to every connected chef/admin screen the moment an order lands."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "new_orders_backend",
        {
            "type": "new_order",  # -> NewOrderConsumer.new_order
            "order": ChefOrderSerializer(order).data,
        },
    )


def broadcast_order_status(order):
    """Pushed only to the one customer this order belongs to."""
    encrypted_phone = order.customer.encrypted_phone  # adjust to your actual relation
    channel_layer = get_channel_layer()
    group_name = channel_group_for(encrypted_phone)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "order_status_update",  # -> OrderConsumer.order_status_update
            "order_id": order.id,
            "status": order.status,
        },
    )