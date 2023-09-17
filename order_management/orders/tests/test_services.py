""" The module holds tests for services in customer module"""
import pytest
from mixer.backend.django import mixer

from order_management.base.tests.test_setup import TestSetUp
from order_management.orders.backend.services import OrderService, OrderItemService

pytestmark = pytest.mark.django_db


class TestOrderService(TestSetUp):
	""" Test Order model service """
	
	def test_get(self):
		""" Test OrderService get method """
		product = mixer.blend('products.Product')
		customer = mixer.blend('customers.Customer')
		mixer.blend('orders.Order', customer=customer, product=product)
		order = OrderService().get(customer=customer)
		assert order is not None, "Should retrieve customer order"
	
	def test_create(self):
		""" Test OrderService create method"""
		product = mixer.blend('products.Product')
		customer = mixer.blend('customers.Customer')
		order = OrderService().create(customer=customer, product=product, total_price=10)
		assert order is not None, "should create order"
		assert order.customer == customer, "Should create order correctly"
	
	def test_filter(self):
		""" Test OrderService filter method """
		mixer.cycle(3).blend('orders.Order')
		orders = OrderService().filter()
		assert orders is not None, "Should retrieve orders"
		assert orders.count() == 3, "should retrieve 3 orders"
	
	def test_update(self):
		""" Test OrderService update method """
		product = mixer.blend('products.Product')
		customer = mixer.blend('customers.Customer')
		order = mixer.blend('orders.Order', customer=customer, product=product, total_price=10)
		updated_order = OrderService().update(order.id, total_price="30")
		assert updated_order.total_price == "30", "Should update order"


class TestOrderItemService(TestSetUp):
	""" Test OrderItem model service """
	
	def test_get(self):
		""" Test OrderItemService get method """
		product = mixer.blend('products.Product')
		order = mixer.blend('orders.Order')
		mixer.blend('orders.OrderItem', order=order, product=product)
		order_item = OrderItemService().get(product=product)
		assert order_item is not None, "Should retrieve customer orderItem"
	
	def test_create(self):
		""" Test OrderItemService create method"""
		product = mixer.blend('products.Product')
		order = mixer.blend('orders.Order')
		order_item = OrderItemService().create(order=order, product=product, total_price=10)
		assert order_item is not None, "should create order item"
		assert order_item.product == product, "Should create order item correctly"
	
	def test_filter(self):
		""" Test OrderItemService filter method """
		mixer.cycle(3).blend('orders.OrderItem')
		order_items = OrderItemService().filter()
		assert order_items is not None, "Should retrieve order items"
		assert order_items.count() == 3, "should retrieve 3 order items"
	
	def test_update(self):
		""" Test OrderItemService update method """
		product = mixer.blend('products.Product')
		order = mixer.blend('orders.Order')
		order_item = mixer.blend('orders.OrderItem', order=order, product=product, total_price=10)
		updated_order_item = OrderItemService().update(order_item.id, total_price="30")
		assert updated_order_item.total_price == "30", "Should update order item"
