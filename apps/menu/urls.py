from django.urls import path

from .views import CategoryListView, FoodItemListView, SubCategoryListView, MenuListView

# app_name = "menu"


urlpatterns = [
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category-list",
    ),

    path(
    "categories/<int:category_id>/items/",
    FoodItemListView.as_view(),
    name="category-food-items",
    ),  

    path(
        "categories/<int:category_id>/subcategories/",
        SubCategoryListView.as_view(),
        name="subcategory-list",
    ),

    path(
        "subcategories/<int:subcategory_id>/items/",
        FoodItemListView.as_view(),
        name="food-item-list",
    ),

    path(
    "",
    MenuListView.as_view(),
    name="menu-list",
),
]