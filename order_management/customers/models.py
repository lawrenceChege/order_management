from django.db import models
from django.contrib.auth.models import User

from base.models import BaseModel


# Create your models here.
class Customer(BaseModel):
	""" Define Customer model"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	code = models.CharField(max_length=10)
	
	def __str__(self):
		return f'{self.user.username}'