from rest_framework import serializers

from order_management.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__All__'