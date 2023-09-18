from django.contrib import admin

from order_management.audit.models import Action


# Register your models here.
@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
	"""
	Action model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = (
	'user', 'action_type', 'reference', 'source_ip', 'request', 'status_code', 'trace', 'description', 'date_modified',
	'date_created')
	search_fields = ('reference',)
