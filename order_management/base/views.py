from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from base.backend.serializers import GroupSerializer, UserSerializer, StateSerializer, CategorySerializer, \
	CurrencySerializer

from .models import State, Category, Currency


class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = [permissions.IsAuthenticated]


class StateViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows states to be viewed or edited.
	"""
	queryset = State.objects.all()
	serializer_class = StateSerializer
	permission_classes = [permissions.IsAuthenticated]
	

class CategoryViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows categories to be viewed or edited.
	"""
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [permissions.IsAuthenticated]
	
	
class CurrencyViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows currencies to be viewed or edited.
	"""
	queryset = Currency.objects.all()
	serializer_class = CurrencySerializer
	permission_classes = [permissions.IsAuthenticated]
