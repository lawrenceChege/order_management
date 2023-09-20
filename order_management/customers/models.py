from django.db import models
from django.contrib.auth.models import User, Group
from base.models import BaseModel, State

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create a new group
default_group, created = Group.objects.get_or_create(name='Customers')


@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
	if created:
		# Assign the user to the default group
		default_group = Group.objects.get(name='Customers')
		instance.groups.add(default_group)


# Create your models here.
class Customer(BaseModel):
	""" Define Customer model"""
	user = models.OneToOneField(User, related_name="customer", on_delete=models.CASCADE)
	status = models.ForeignKey(State, default=State.default_state(), on_delete=models.CASCADE)
	
	def __str__(self):
		return f'{self.code}'
