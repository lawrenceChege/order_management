from django.contrib import admin

from .models import Customer


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	"""
	Customer model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('user', 'code', 'date_modified', 'date_created')
	search_fields = ('user__first_name',)