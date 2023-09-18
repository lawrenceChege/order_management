""" Services for Orders module"""
from base.backend.service_base import ServiceBase
from ..models import Order, OrderItem


class OrderService(ServiceBase):
	""" Defines CRUD for Order Model """
	manager = Order.objects


class OrderItemService(ServiceBase):
	""" Defines CRUD for OrderItem model"""
	manager = OrderItem.objects
