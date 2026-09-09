from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import CafeTable
from .serializers import CafeTableSerializer


class CafeTableListView(generics.ListAPIView):
    serializer_class = CafeTableSerializer

    def get_queryset(self):
        queryset = CafeTable.objects.prefetch_related(
            "images"
        ).filter(
            is_active=True,
            is_available=True,
        )

        guests = self.request.query_params.get(
            "guests"
        )

        if guests:
            try:
                guests = int(guests)

                if guests > 0:
                    queryset = queryset.filter(
                        capacity__gte=guests
                    )

            except (TypeError, ValueError):
                pass

        return queryset