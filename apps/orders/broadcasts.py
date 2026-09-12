from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .channels_utils import channel_group_for
from .serializers import ChefOrderSerializer


CHEF_GROUP = "new_orders_backend"


def broadcast_new_order(order):
    """
    Broadcast a newly created order to
    all connected chef/admin screens.
    """

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
    """
    Broadcast status to:

    1. The customer who owns the order
    2. Every connected chef/admin screen
    """

    channel_layer = get_channel_layer()

    # ---------------------------------
    # Customer
    # ---------------------------------

    encrypted_phone = (
        order.customer.encrypted_phone
    )

    customer_group = channel_group_for(
        encrypted_phone
    )

    async_to_sync(
        channel_layer.group_send
    )(
        customer_group,
        {
            "type":
                "order_status_update",

            "order_id":
                order.id,

            "status":
                order.status,
        },
    )


    # ---------------------------------
    # Kitchen / Admin
    # ---------------------------------

    async_to_sync(
        channel_layer.group_send
    )(
        CHEF_GROUP,
        {
            "type":
                "order_status_update",

            "order":
                ChefOrderSerializer(
                    order
                ).data,
        },
    )