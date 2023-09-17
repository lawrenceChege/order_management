""" The module holds tests for services in customer module"""
import pytest
from mixer.backend.django import mixer

from order_management.base.tests.test_setup import TestSetUp
from order_management.customers.backend.services import CustomerService

pytestmark = pytest.mark.django_db


class TestCustomerService(TestSetUp):
	""" Test Customer model service """
	
	def test_get(self):
		""" Test CustomerService get method """
		mixer.blend('customers.Customer', username="larry")
		customer = CustomerService().get(username="larry")
		assert customer is not None, "Should retrieve customer"
		
	def test_create(self):
		""" Test CustomerService create method"""
		customer = CustomerService().create(username="larry", email="larry@gmail.com", password="larry_password")
		assert customer is not None, "should create customer"
		assert customer.email == "larry@gmail.com", "Should create user correctly"
		
	def test_filter(self):
		""" Test CustomerService filter method """
		mixer.cycle(3).blend('customers.Customer')
		customers = CustomerService().filter()
		assert customers is not None, "Should retrieve customers"
		assert customers.count() == 3, "should retrieve 3 customers"
		
	def test_update(self):
		""" Test CustomerService update method """
		customer = mixer.blend('customers.Customer', username="larry", email="larry@gmail.com", password="larry_password")
		updated_customer = CustomerService().update(customer.id, password="12345678")
		assert updated_customer.password == "12345678", "Should update customer"
		
		