"""
Base Models
"""
from uuid import uuid4

# from uuid_extensions import uuid7
from django.utils import timezone
from django.db import models


class BaseModel(models.Model):
	"""
	Define the basic structure of a model
	"""
	synced = models.BooleanField(default=False)
	id = models.UUIDField(max_length=50, default=uuid4(), unique=True, editable=False, primary_key=True)
	date_modified = models.DateTimeField(auto_now=True)  # (default = timezone.now)
	date_created = models.DateTimeField(auto_now_add=True)  # (default = timezone.now)

	SYNC_MODEL = False

	class Meta(object):
		abstract = True


class NamedModel(BaseModel):
	"""
	Define any model with a name and a description
	"""
	name = models.CharField(max_length=35, null=False)
	description = models.TextField(max_length=255, blank=True, null=True)

	class Meta(object):
		abstract = True


class State(NamedModel):
	"""
	States for objects lifecycle e.g. "Active", "Deleted", "Disabled", etc
	"""
	
	def __str__(self):
		return '%s' % self.name

	SYNC_MODEL = True

	class Meta(object):
		ordering = ('name',)
		unique_together = ('name',)

	@classmethod
	def default_state(cls):
		"""
	The default Active state. Help in ensuring that the admin will be created without supplying the state at the
	command like.
	@return: The active state, if it exists, or create a new one if it doesn't exist.
	@rtype: str | None
	"""
		# noinspection PyBroadException
		state_active = cls.objects.filter(name="Active").first()
		state = state_active if state_active else cls.objects.create(id="f1c6100d-64b2-48cd-be83-deb21e1c26c6", name="Active")
		return state.id

	@classmethod
	def disabled_state(cls):
		"""
		The default Disabled state. Help in ensuring that the admin will be created without supplying the state at the
		command like.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
		# noinspection PyBroadException

		state = cls.objects.get(name='Disabled')
		return state


class Currency(NamedModel):
	"""
	Defines a type of Currency and its code e.g US Dollar - USD
	"""

	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)
	code = models.CharField(max_length=10)

	def __str__(self):
		return '%s - %s' % (self.name, self.code)

	class Meta(NamedModel.Meta):
		verbose_name_plural = 'Currencies'
		unique_together = ('name',)
		

class Category(NamedModel):
	"""
	Defines a category and its code e.g Clothing, Food, Toys
	"""

	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)
	
	def __str__(self):
		return '%s' % (self.name,)

	class Meta(NamedModel.Meta):
		verbose_name_plural = 'Categories'
		unique_together = ('name',)