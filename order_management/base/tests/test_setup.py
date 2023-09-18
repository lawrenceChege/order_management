import json

from mixer.backend.django import mixer
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

# DJANGO_SETTINGS_MODULE = order_management.order_management.test_settings


class TestSetUp(APITestCase):
	"""
		Setup data for Customer Models
	"""
	
	def setUp(self):
		self.client = APIClient()
		self.factory = APIRequestFactory()
		# self.state = mixer.blend('base.State', name="Active")
	
	def tearDown(self):
		return super().tearDown()
