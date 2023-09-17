from django.contrib import admin

from .models import OrderItem, Order


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	"""
	Order model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('customer', 'total_price', 'date_modified', 'date_created')
	search_fields = ('name',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	"""
	Order Ite, model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('order', 'product', 'quantity', 'total_price', 'date_modified', 'date_created')
	search_fields = ('product__name',)
