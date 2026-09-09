from django.contrib import admin

from .models import CafeTable, CafeTableImage


class CafeTableImageInline(
    admin.TabularInline
):
    model = CafeTableImage
    extra = 1


@admin.register(CafeTable)
class CafeTableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "table_number",
        "capacity",
        "is_available",
        "is_active",
        # "display_order",
    )

    list_filter = (
        "is_available",
        "is_active",
        "capacity",
    )

    search_fields = (
        "table_number",
    )

    inlines = [
        CafeTableImageInline,
    ]


@admin.register(CafeTableImage)
class CafeTableImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "table",
        # "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )