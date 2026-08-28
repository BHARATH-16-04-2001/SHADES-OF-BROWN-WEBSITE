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
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import generics

from .models import (
    Category,
    FoodItem,
    FoodItemImage,
    SubCategory,
)

class FoodItemListView(APIView):

    def get(self, request, category_id=None, subcategory_id=None):

        if category_id:
            items = FoodItem.objects.filter(
                subcategory__category_id=category_id
            )

        elif subcategory_id:
            items = FoodItem.objects.filter(
                subcategory_id=subcategory_id
            )

        else:
            items = FoodItem.objects.all()

        serializer = FoodItemSerializer(items, many=True)

        return Response(serializer.data)


class FoodItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItemImage
        fields = [
            "id",
            "image",
            "alt_text",
            "display_order",
        ]
# class FoodItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FoodItem
#         fields = "__all__"

class FoodItemSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True
    )

    category_id = serializers.IntegerField(
        source="subcategory.category.id",   
        read_only=True
    )

    category_name = serializers.CharField(
        source="subcategory.category.name",
        read_only=True
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
            "is_available",
            "is_featured",
            "preparation_time",
            "display_order",
            "subcategory",
            "subcategory_name",
            "category_name",
            "category_id",
            "created_at",
            "updated_at",
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

class FoodItemHomeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="subcategory.category.name",
        read_only=True
    )
    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True
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
            "category_name",
            "subcategory_name",
            "is_available",
            "is_featured",
            "preparation_time",
        ]
