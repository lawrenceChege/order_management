from django.test import TestCase
from .models import Customer, Order


class CustomerOrderModelTestCase(TestCase):
	def setUp(self):
		self.customer = Customer.objects.create(name='John', code='C123', phone_number="098765412")
		self.order = Order.objects.create(
			customer=self.customer,
			item='Item1',
			amount=100.0,
			time='2023-09-20T12:00:00'
		)
	
	def test_customer_creation(self):
		self.assertEqual(self.customer.name, 'John')
		self.assertEqual(self.customer.code, 'C123')
		self.assertEqual(self.customer.phone_number, '098765412')
	
	def test_order_creation(self):
		self.assertEqual(self.order.customer, self.customer)
		self.assertEqual(self.order.item, 'Item1')
		self.assertEqual(self.order.amount, 100.0)
