from django.db import models
from order_management.base.models import BaseModel, State, NamedModel, Currency, Category


class Product(NamedModel):
	"""
	Defines model
	"""
	category = models.ForeignKey(Category, on_delete=models.CASCADE())
	price = models.DecimalField(verbose_name="Price of product", max_digits=25, decimal_places=2, default=0.00)
	quantity = models.IntegerField(verbose_name="Number of products", max_length=25)
	currency = models.ForeignKey(Currency, on_delete=models.CASCADE())
	status = models.ForeignKey(State, default=State.default_state,  on_delete=models.CASCADE())
	
	class Meta(BaseModel.Meta):
		verbose_name_plural = 'Products'
	
	def __repr__(self):
		return f'Name: {self.name}, Amount:{self.currency.code} {self.amount} '
	
	def __str__(self):
		return f'{self.name} is {self.status}'
