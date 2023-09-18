import pytest
from mixer.backend.django import mixer

from base.tests.test_setup import TestSetUp

pytestmark = pytest.mark.django_db


class TestOrderModel(TestSetUp):
	"""
	Test Order module models
	"""
	
	def test_order(self):
		obj = mixer.blend('orders.Order')
		assert obj is not None, "Should create order"
		assert obj.__str__() == '%s ' % (obj.total_price,)
		
	def test_orderItem(self):
		obj = mixer.blend('orders.OrderItem')
		assert obj is not None, "Should create orderItem"
		assert obj.__str__() == '%s - %s' % (obj.product.name, obj.quantity)
