"""
Model managers for models in this Base Module.
Managers allow for smooth CRUD operations
"""
from .service_base import ServiceBase
from ..models import State, Currency, Category


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