from rest_framework import serializers

from .models import Customer


# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = [
#             "id",
#             "name",
#             "phone",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = [
#             "id",
#             "created_at",
#             "updated_at",
#         ]

#     def validate_name(self, value):
#         value = value.strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Name is required."
#             )

#         return value

#     def validate_phone(self, value):
#         # value = value.strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Phone number is required."
#             )

#         return value  

import re

from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        max_length=10,
        min_length=10,
        required=True,
        allow_blank=False,
    )

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Name is required."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if not re.fullmatch(r"[6-9]\d{9}", value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit Indian mobile number."
            )

        return value