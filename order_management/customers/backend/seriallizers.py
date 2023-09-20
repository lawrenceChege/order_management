from rest_framework import serializers

from base.backend.serializers import UserSerializer, StateSerializer
from customers.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer()
	status = StateSerializer()
	
	class Meta:
		model = Customer
		fields = '__all__'
