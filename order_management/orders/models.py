from django.db import models
from base.models import BaseModel, State, NamedModel
from customers.models import Customer

from products.models import Product


class Order(BaseModel):
	"""
	Defines customer order
	"""
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	products = models.ManyToManyField(Product, through='OrderItem')
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)
	
	def __str__(self):
		return '%s ' % (self.total_price,)


class OrderItem(BaseModel):
	"""
	Defines an item in the order
	"""
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
	
	def __str__(self):
		return '%s - %s' % (self.product.name, self.quantity)
	
	class Meta:
		unique_together = ['order', 'product']

