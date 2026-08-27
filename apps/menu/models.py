from django.db import models


class Category(models.Model):
  
    # Main menu category.

    # Examples:
    # - Coffee
    # - Sandwich
    # - Burgers
    # - Pizza
    # - Desserts
  

    name = models.CharField(
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        blank=True,
    )
    image = models.ImageField(
        upload_to="menu/categories/",
        blank=True,
        null=True,
    )
    display_order = models.PositiveIntegerField(
        default=0,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """
    # Subcategory belonging to a main Category.

    # Examples:

    # Coffee
    #     - Hot Coffee
    #     - Cold Coffee

    # Burgers
    #     - Veg
    #     - Non-Veg

    # Pizza
    #     - Veg Pizza
    #     - Non-Veg Pizza
    # """

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="subcategories",
    )
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        blank=True,
    )
    image = models.ImageField(
        upload_to="menu/subcategories/",
        blank=True,
        null=True,
    )
    display_order = models.PositiveIntegerField(
        default=0,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["display_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_subcategory_per_category",
            ),
        ]
        indexes = [
            models.Index(
                fields=["category", "is_active"],
            ),
        ]

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class FoodItem(models.Model):
    """
    Individual food/menu item.

    A FoodItem belongs to a SubCategory.
    """

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        related_name="food_items",
    )
    name = models.CharField(
        max_length=150,
    )
    description = models.TextField(
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="menu/items/",
        blank=True,
        null=True,
    )
    is_available = models.BooleanField(
        default=True,
    )
    is_featured = models.BooleanField(
        default=False,
    )
    preparation_time = models.PositiveIntegerField(
        default=0,
        help_text="Preparation time in minutes.",
    )
    display_order = models.PositiveIntegerField(
        default=0,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["display_order", "name"]
        indexes = [
            models.Index(
                fields=["subcategory", "is_available"],
            ),
            models.Index(
                fields=["is_featured", "is_available"],
            ),
        ]

    def __str__(self):
        return self.name


class FoodItemImage(models.Model):
    """
    Additional images for a FoodItem.

    A food item can have multiple images.
    """

    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        upload_to="menu/items/gallery/",
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
    )
    display_order = models.PositiveIntegerField(
        default=0,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.food_item.name} image"

