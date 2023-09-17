import pytest
from mixer.backend.django import mixer

from order_management.base.tests.test_setup import TestSetUp

pytestmark = pytest.mark.django_db


class TestCustomerModel(TestSetUp):
	"""
	Test customer module models
	"""
	
	def test_customer(self):
		obj = mixer.blend('customers.Customer')
		assert obj is not None, "Should create customer"
