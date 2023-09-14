import json

from mixer.backend.django import mixer
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.urls import reverse


class TestSetUp(APITestCase):
	def setUp(self):
		self.client = APIClient()
		self.factory = APIRequestFactory()
		self.state_active = mixer.blend('base.State',name="Active")
		self.state_approval_pending = mixer.blend('base.State',name="Approval pending")
		self.state_deleted = mixer.blend('base.State',name="Deleted")

	def tearDown(self):
		return super().tearDown()


