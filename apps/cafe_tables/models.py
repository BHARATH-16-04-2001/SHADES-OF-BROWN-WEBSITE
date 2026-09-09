from django.db import models
from django.utils import timezone


class CafeTable(models.Model):
    table_number = models.PositiveIntegerField(
        unique=True,
    )

    capacity = models.PositiveIntegerField(
        help_text="Maximum number of people this table can accommodate.",
    )

    is_available = models.BooleanField(
        default=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    description = models.TextField(
        blank=True,
        default="",
    )

    # display_order = models.PositiveIntegerField(
    #     default=0,
    # )

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    updated_at = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        ordering = [
            # "display_order",
            "table_number",
        ]

    def __str__(self):
        return f"Table {self.table_number}"



class CafeTableImage(models.Model):
    table = models.ForeignKey(
        CafeTable,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="cafe_tables/",
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True,
        default="",
    )

    # display_order = models.PositiveIntegerField(
    #     default=0,
    # )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
            default=timezone.now,
            editable=False,
        )

    class Meta:
        ordering = [
            # "display_order",
            "id",
        ]

    def __str__(self):
        return f"Table {self.table.table_number} image"