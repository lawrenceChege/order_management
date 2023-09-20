from rest_framework import viewsets
from rest_framework import permissions
from .backend.serializers import OrderItemSerializer, OrderSerializer

from .models import OrderItem, Order


class OrderViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows orders to be viewed or edited.
	"""
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [permissions.IsAuthenticated]


class OrderItemViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows order items to be viewed or edited.
	"""
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer
	permission_classes = [permissions.IsAuthenticated]



