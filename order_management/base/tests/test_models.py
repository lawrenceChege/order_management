import pytest
from mixer.backend.django import mixer

import order_management.base.models
from order_management.base.tests.test_setup import TestSetUp

pytestmark = pytest.mark.django_db


class TestBaseModels(TestSetUp):
	"""
	Test base module models
	"""
	
	def test_state_str(self):
		"""Test for state model"""
		obj = mixer.blend('order_management.base.State')
		assert obj is not None, "Should create instance of state"
		assert obj.__str__() == obj.name, "Should return state name"
		
	def test_state_disable(self):
		"""Test for state model disabled state"""
		state = mixer.blend('order_management.base.models.State')
		obj = state.disabled_state()
		self.assertEqual(obj.name, "Disabled"), "Should return disabled state"
		
	def test_currency(self):
		"""Test for currency model"""
		obj = mixer.blend('order_management.base.Currency', name='Kenya Shilling', code='KSH')
		assert obj is not None, "Should create currency"
		assert obj.__str__() == '%s - %s' % (obj.name, obj.code)
		
	def test_category(self):
		"""Test for category model"""
		obj = mixer.blend('order_management.base.Category', name="Foodstuffs")
		assert obj is not None, "Should create a category"
		assert obj.__str__() == '%s' % (obj.name,)
