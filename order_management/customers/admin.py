from django.contrib import admin

from .models import Customer


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	"""
	Customer model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_joined',)
	list_display = ('first_name', 'code')
	search_fields = ('first_name',)