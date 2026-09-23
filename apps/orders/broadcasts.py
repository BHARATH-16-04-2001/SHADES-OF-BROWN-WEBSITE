

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .channels_utils import channel_group_for
from .serializers import ChefOrderSerializer


CHEF_GROUP = "new_orders_backend"


def broadcast_new_order(order):

    channel_layer = get_channel_layer()

    async_to_sync(
        channel_layer.group_send
    )(
        CHEF_GROUP,
        {
            "type": "new_order",
            "order": ChefOrderSerializer(
                order
            ).data,
        },
    )


def broadcast_order_status(order):

    channel_layer = get_channel_layer()

    # -----------------------------------------
    # Customer group
    # -----------------------------------------

    encrypted_phone = (
        order.customer.encrypted_phone
    )

    customer_group = channel_group_for(
        encrypted_phone
    )

    # -----------------------------------------
    # Send update to customer
    # -----------------------------------------

    async_to_sync(
        channel_layer.group_send
    )(
        customer_group,
        {
            "type": "order_status_update",

            # IMPORTANT
            # Use orderId
            "order_id": order.id,

            "status": order.status,
        },
    )

    # -----------------------------------------
    # Send update to all admin/chef screens
    # -----------------------------------------

    async_to_sync(
        channel_layer.group_send
    )(
        CHEF_GROUP,
        {
            "type": "order_status_update",

            "order": ChefOrderSerializer(
                order
            ).data,
        },
    )