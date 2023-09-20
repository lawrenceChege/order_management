from django.contrib.auth.models import User, Group
from rest_framework import serializers

from base.models import Category, Currency, State


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ['url', 'name']


class StateSerializer(serializers.ModelSerializer):
	class Meta:
		model = State
		fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
	class Meta:
		model = Currency
		fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'
