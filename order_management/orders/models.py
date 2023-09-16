from django.db import models
from order_management.base.models import BaseModel, State, NamedModel
from order_management.customers.models import Customer

from order_management.products.models import Product


class Order(BaseModel):
	"""
	Defines customer order
	"""
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE())
	products = models.ManyToManyField(Product, through='OrderItem')
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE())


class OrderItem(BaseModel):
	"""
	Defines an item in the order
	"""
	order = models.ForeignKey(Order, on_delete=models.CASCADE())
	product = models.ForeignKey(Product, on_delete=models.CASCADE())
	quantity = models.PositiveIntegerField(default=1)
	
	class Meta:
		unique_together = ('order, product')
