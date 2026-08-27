from django.contrib import admin

from .models import (
    Category,
    FoodItem,
    FoodItemImage,
    SubCategory,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "display_order",
        "created_at",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = (
        "display_order",
        "name",
    )


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "is_active",
        "display_order",
        "created_at",
    )
    list_filter = (
        "category",
        "is_active",
    )
    search_fields = (
        "name",
        "description",
        "category__name",
    )
    ordering = (
        "category",
        "display_order",
        "name",
    )


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "subcategory",
        "price",
        "discount_price",
        "is_available",
        "is_featured",
        "preparation_time",
    )
    list_filter = (
        "is_available",
        "is_featured",
        "subcategory__category",
        "subcategory",
    )
    search_fields = (
        "name",
        "description",
        "subcategory__name",
        "subcategory__category__name",
    )
    ordering = (
        "subcategory",
        "display_order",
        "name",
    )


@admin.register(FoodItemImage)
class FoodItemImageAdmin(admin.ModelAdmin):
    list_display = (
        "food_item",
        "display_order",
        "created_at",
    )
    list_filter = (
        "food_item__subcategory__category",
    )
    search_fields = (
        "food_item__name",
        "alt_text",
    )
    ordering = (
        "food_item",
        "display_order",
    )