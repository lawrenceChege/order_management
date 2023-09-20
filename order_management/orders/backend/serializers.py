from rest_framework import serializers

from customers.backend.seriallizers import CustomerSerializer
from orders.models import Order, OrderItem
from products.backend.seriallizers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
	customer = CustomerSerializer()
	products = ProductSerializer(many=True)
	
	class Meta:
		model = Order
		fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
	order = OrderSerializer()
	product = ProductSerializer()
	
	class Meta:
		model = OrderItem
		fields = '__all__'
