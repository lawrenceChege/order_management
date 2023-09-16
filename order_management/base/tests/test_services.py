"""
This module holds tests for the services in base module
"""

import pytest
from mixer.backend.django import mixer

from order_management.base.backend.services import StateService
from order_management.base.tests.test_setup import TestSetUp

pytestmark = pytest.mark.django_db


class TestStateService(TestSetUp):
	""" Test the state model service"""
	def test_get(self):
		""" Test StateService get method """
		mixer.blend('order_management.base.State')
		state = StateService().get(name="Active")
		assert state is not None, "Default state should be Active"
		
	def test_create(self):
		""" Test StateService create method """
		approved = StateService().create(name="approved")
		assert approved is not None, "Should create approved state"
		assert approved.__str__() == "approved", "Should create state correctly"
		
	def test_filter(self):
		""" Test StateService filter method """
		mixer.cycle(3).blend('order_management.base.State')
		states = StateService().filter()
		assert states is not None, "Should retrieve states"
		assert states.count() == 3, "Should have 3 states"
		
	def test_update(self):
		""" Test StateService update method """
		state = mixer.blend('order_management.base.State', name="Approval Pending")
		updated_state = StateService().update(state.id, name="Pending approval")
		assert updated_state.name == "Pending approval", "Should update state"
		
		