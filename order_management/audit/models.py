from django.contrib.auth.models import User
from django.db import models, transaction

from base.models import NamedModel, State, BaseModel

from audit.backend.generate_code import generate_internal_reference


class ActionType(NamedModel):
	""" Defines an action in the system"""
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)
	
	def __str__(self):
		return '%s %s' % (self.name, self.state)
	
	class Meta(NamedModel.Meta):
		unique_together = ('name',)


class Action(BaseModel):
	""" Keeps a record of all actions in the system"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='Action_By')
	action_type = models.ForeignKey(ActionType, on_delete=models.CASCADE)
	reference = models.CharField(max_length=20, unique=True)
	source_ip = models.GenericIPAddressField(max_length=20, null=True, blank=True)
	request = models.JSONField(null=True, blank=True)
	status_code = models.CharField(max_length=10, default='000.000.000')
	trace = models.FilePathField(allow_folders=True)
	description = models.TextField(max_length=300, null=True, blank=True)
	is_client_viewable = models.BooleanField(default=False)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)
	
	SYNC_MODEL = False
	
	class Meta(object):
		verbose_name_plural = "Actions"
		unique_together = ('action_type', 'reference')
		
	def __str__(self):
		return f'{self.action_type} status {self.status_code}'
	
	@classmethod
	def next_reference(cls, retries=0):
		"""
		Retrieves the current action in the DB to pass to the generator after locking the selected ID.
		This then attempts to generate a unique reference for use with the next action.
		@param retries: The number of times we have retried generating a unique reference.
		@type retries: int
		@return: The generated Reference.
		@rtype: str | None
		"""
		with transaction.atomic():
			last_action = cls.objects.select_for_update().order_by('-date_created').first()
			ref = generate_internal_reference(last_action.reference if last_action else None)
			if cls.objects.filter(reference=ref).exists() and retries < 20:
				retries += 1
				return cls.next_reference(retries)
			return ref
		
	

		
