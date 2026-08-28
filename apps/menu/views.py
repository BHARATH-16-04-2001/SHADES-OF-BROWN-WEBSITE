from rest_framework.generics import ListAPIView
from django.db.models import Prefetch
from .models import Category, SubCategory, FoodItem
from .serializers import CategorySerializer, SubCategorySerializer, FoodItemSerializer, MenuCategorySerializer, FoodItemHomeSerializer
from rest_framework import generics


class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(
        is_active=True
    )
    serializer_class = CategorySerializer


class SubCategoryListView(ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        category_id = self.kwargs["category_id"]

        return SubCategory.objects.filter(
            category_id=category_id,
            is_active=True,
        )

class FoodItemListView(ListAPIView):
    serializer_class = FoodItemSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs["subcategory_id"]

        return (
            FoodItem.objects
            .filter(
                subcategory_id=subcategory_id,
                is_available=True,
            )
            .prefetch_related("images")
        )

class MenuListView(ListAPIView):
    serializer_class = MenuCategorySerializer

    def get_queryset(self):
        available_items = (
            FoodItem.objects
            .filter(is_available=True)
            .prefetch_related("images")
            .order_by("display_order", "name")
        )

        active_subcategories = (
            SubCategory.objects
            .filter(is_active=True)
            .prefetch_related(
                Prefetch(
                    "food_items",
                    queryset=available_items,
                )
            )
            .order_by("display_order", "name")
        )

        return (
            Category.objects
            .filter(is_active=True)
            .prefetch_related(
                Prefetch(
                    "subcategories",
                    queryset=active_subcategories,
                )
            )
            .order_by("display_order", "name")
        )

class FoodItemListView(generics.ListAPIView):
    serializer_class = FoodItemSerializer

    def get_queryset(self):
        if "category_id" in self.kwargs:
            category_id = self.kwargs["category_id"]

            return FoodItem.objects.filter(
                subcategory__category_id=category_id
            )

        if "subcategory_id" in self.kwargs:
            subcategory_id = self.kwargs["subcategory_id"]

            return FoodItem.objects.filter(
                subcategory_id=subcategory_id
            )

        return FoodItem.objects.all()


class HomeFoodItemListView(generics.ListAPIView):
    serializer_class = FoodItemHomeSerializer

    def get_queryset(self):
        return FoodItem.objects.select_related(
            "subcategory",
            "subcategory__category"
        ).filter(
            is_available=True
        ).order_by(
            "display_order"
        )