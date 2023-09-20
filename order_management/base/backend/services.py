"""
Model managers for models in this Base Module.
Managers allow for smooth CRUD operations
"""
from django.contrib.auth.models import Group, User

from .service_base import ServiceBase
from ..models import State, Currency, Category


class UserService(ServiceBase):
	""" Service for User module """
	manager = User.objects


class GroupService(ServiceBase):
	""" Service for User Groups module """
	manager = Group.objects


class StateService(ServiceBase):
	"""
	Service for State Model
	"""
	manager = State.objects


class CurrencyService(ServiceBase):
	"""
	Service for Currency Model
	"""
	manager = Currency.objects


class CategoryService(ServiceBase):
	"""
	Service for Category Model
	"""
	manager = Category.objects
