from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer


class CustomerListCreateView(generics.ListCreateAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer


class OrderListCreateView(generics.ListCreateAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	authentication_classes = [SessionAuthentication]  # Use the appropriate authentication method
	permission_classes = [IsAuthenticated]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	authentication_classes = [SessionAuthentication]  # Use the appropriate authentication method
	permission_classes = [IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer


class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	authentication_classes = [SessionAuthentication]  # Use the appropriate authentication method
	permission_classes = [IsAuthenticated]

