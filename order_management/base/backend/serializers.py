from rest_framework import serializers

from base.models import Category, Currency, State


class StateSerializer(serializers.ModelSerializer):
	class Meta:
		model = State
		fields = '__All__'


class CurrencySerializer(serializers.ModelSerializer):
	class Meta:
		model = Currency
		fields = '__All__'


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__All__'
