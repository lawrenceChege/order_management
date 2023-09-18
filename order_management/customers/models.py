from django.db import models
from django.contrib.auth.models import User, AbstractUser

from base.models import BaseModel


# Create your models here.
class Customer(User):
	""" Define Customer model"""
	def __int__(self):
		super(Customer, self).__int__()
		
	# user = models.OneToOneField(User, related_name="customer", on_delete=models.CASCADE)
	code = models.CharField(max_length=10)
	
	def __str__(self):
		return f'{self.user.username}'