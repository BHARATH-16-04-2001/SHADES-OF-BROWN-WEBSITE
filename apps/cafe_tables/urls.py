from django.urls import path

from .views import CafeTableListView


app_name = "cafe_tables"


urlpatterns = [
    path(
        "",
        CafeTableListView.as_view(),
        name="table-list",
    ),
]