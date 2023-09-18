"""
This module holds tests for the services in base module
"""

import pytest
from mixer.backend.django import mixer

from ..backend.services import StateService, CurrencyService, CategoryService
from .test_setup import TestSetUp

pytestmark = pytest.mark.django_db


class TestStateService(TestSetUp):
	""" Test the state model service"""
	
	def test_get(self):
		""" Test StateService get method """
		mixer.blend('base.State')
		state = StateService().get(name="Active")
		assert state is not None, "Default state should be Active"
	
	def test_create(self):
		""" Test StateService create method """
		approved = StateService().create(name="approved")
		assert approved is not None, "Should create approved state"
		assert approved.__str__() == "approved", "Should create state correctly"
	
	def test_filter(self):
		""" Test StateService filter method """
		mixer.cycle(3).blend('base.State')
		states = StateService().filter()
		assert states is not None, "Should retrieve states"
		assert states.count() == 3, "Should have 3 states"
	
	def test_update(self):
		""" Test StateService update method """
		state = mixer.blend('base.State', name="Approval Pending")
		updated_state = StateService().update(state.id, name="Pending approval")
		assert updated_state.name == "Pending approval", "Should update state"


class TestCurrencyService(TestSetUp):
	""" Test the Currency model service"""
	
	def test_create(self):
		""" Test CurrencyService create method """
		usd = CurrencyService().create(name="US Dollar", code='USD')
		assert usd is not None, "Should create currency"
		assert usd.name == "US Dollar", "Should create currency correctly"
	
	def test_get(self):
		""" Test CurrencyService get method """
		mixer.blend('base.Currency', name='Kenya Shilling', code='KSH')
		currency = CurrencyService().get(code="KSH")
		assert currency is not None, "Should retrieve currency"
	
	def test_filter(self):
		""" Test CurrencyService filter method """
		mixer.cycle(3).blend('base.Currency')
		currencies = CurrencyService().filter()
		assert currencies is not None, "Should retrieve currencies"
		assert currencies.count() == 3, "Should have 3 currencies"
	
	def test_update(self):
		""" Test CurrencyService update method """
		euro = mixer.blend('base.Currency', name="Euro", code='$')
		updated_euro = CurrencyService().update(euro.id, code="€")
		assert updated_euro.name == "€", "Should update currency"


class TestCategoryService(TestSetUp):
	""" Test the Category model service"""
	
	def test_create(self):
		""" Test CategoryService create method """
		food = CategoryService().create(name="Food")
		assert food is not None, "Should create category"
		assert food.name == "Food", "Should create category correctly"
	
	def test_get(self):
		""" Test CategoryService get method """
		mixer.blend('base.Category', name='Clothing')
		category = CategoryService().get(name="Clothing")
		assert category is not None, "Should retrieve category"
	
	def test_filter(self):
		""" Test CategoryService filter method """
		mixer.cycle(3).blend('base.Category')
		categories = CategoryService().filter()
		assert categories is not None, "Should retrieve categories"
		assert categories.count() == 3, "Should have 3 categories"
	
	def test_update(self):
		""" Test CategoryService update method """
		category = mixer.blend('base.Currency', name="Food")
		updated_category = CategoryService().update(category.id, name="Food and Beverages")
		assert updated_category.name == "Food and Beverages", "Should update category"
