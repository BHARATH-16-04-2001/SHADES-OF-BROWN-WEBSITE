# from rest_framework import serializers

# from .models import Category, SubCategory, FoodItem, FoodItemImage


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = [
#             "id",
#             "name",
#             "description",
#             "image",
#             "display_order",
#             "is_active",
#         ]

# class SubCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubCategory
#         fields = [
#             "id",
#             "name",
#             "description",
#             "image",
#             "display_order",
#             "is_active",
#         ]


# class FoodItemImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FoodItemImage
#         fields = [
#             "id",
#             "image",
#             "alt_text",
#             "display_order",
#         ]      

# class FoodItemSerializer(serializers.ModelSerializer):
#     images = FoodItemImageSerializer(
#         many=True,
#         read_only=True,
#     )

#     class Meta:
#         model = FoodItem
#         fields = [
#             "id",
#             "name",
#             "description",
#             "price",
#             "discount_price",
#             "image",
#             "images",
#             "is_available",
#             "is_featured",
#             "preparation_time",
#             "display_order",
#         ]


from rest_framework import serializers

from .models import (
    Category,
    FoodItem,
    FoodItemImage,
    SubCategory,
)


class FoodItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItemImage
        fields = [
            "id",
            "image",
            "alt_text",
            "display_order",
        ]


class FoodItemSerializer(serializers.ModelSerializer):
    images = FoodItemImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = FoodItem
        fields = [
            "id",
            "name",
            "description",
            "price",
            "discount_price",
            "image",
            "images",
            "is_available",
            "is_featured",
            "preparation_time",
            "display_order",
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            "id",
            "name",
            "description",
            "image",
            "display_order",
            "is_active",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "image",
            "display_order",
            "is_active",
        ]


class MenuFoodItemSerializer(FoodItemSerializer):
    pass


class MenuSubCategorySerializer(serializers.ModelSerializer):
    items = MenuFoodItemSerializer(
        source="food_items",
        many=True,
        read_only=True,
    )

    class Meta:
        model = SubCategory
        fields = [
            "id",
            "name",
            "description",
            "image",
            "display_order",
            "is_active",
            "items",
        ]


class MenuCategorySerializer(serializers.ModelSerializer):
    subcategories = MenuSubCategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "image",
            "display_order",
            "is_active",
            "subcategories",
        ]