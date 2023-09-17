from django.contrib import admin

from .models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	"""
	Product model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'price', 'quantity', 'date_modified', 'date_created')
	search_fields = ('name',)
