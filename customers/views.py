from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from .models import Customer
from .serializers import CustomerSerializer


class CustomerCreateView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetailView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer