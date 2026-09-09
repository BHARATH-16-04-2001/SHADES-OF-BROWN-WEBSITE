from rest_framework import serializers

from .models import CafeTable, CafeTableImage


class CafeTableImageSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = CafeTableImage
        fields = [
            "id",
            "image",
            "alt_text",
            # "display_order",
        ]


class CafeTableSerializer(
    serializers.ModelSerializer
):
    images = CafeTableImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CafeTable
        fields = [
            "id",
            "table_number",
            "capacity",
            "description",
            "images",
            "is_available",
            "is_active",
            # "display_order",
        ]