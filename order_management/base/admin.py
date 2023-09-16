from django.contrib import admin

from order_management.base.models import State, Currency, Category


# Register your models here.
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
	"""
	State model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
	"""
	Currency model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'code', 'description', 'date_modified', 'date_created')
	search_fields = ('name', 'code')
	

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	"""
	Category model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)
	
