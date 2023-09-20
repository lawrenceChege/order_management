from rest_framework import serializers

from base.backend.serializers import UserSerializer, StateSerializer
from customers.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer(read_only=True)
	status = StateSerializer(read_only=True)
	
	class Meta:
		model = Customer
		fields = '__all__'
