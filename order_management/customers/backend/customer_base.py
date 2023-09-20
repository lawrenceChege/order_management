"""
This module has helper methods for customer views
"""

import logging
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import validate_email
from django.http import JsonResponse, HttpRequest

from audit.backend.action_log_base import ActionLogBase
from base.backend.get_request_data import get_request_data
from base.backend.services import StateService, UserService, GroupService
from base.backend.validators import validate_uuid7, validate_name, validate_password
from customers.backend.seriallizers import CustomerSerializer
from customers.backend.services import CustomerService

lgr = logging.getLogger(__name__)


class CustomerBase(ActionLogBase):
	"""
	This class handles the methods for creating, updating, reading and deleting
	customers
	"""

	def add_customer(self, request) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles creating of a customer
		@params request: Http request
		@type request: HttpRequest
		@return Json response
		"""
		action = self.log_action(
			action_type="Add Customer", trace="customer_base/add_customer", request=request)
		try:
			if action is None:
				return {'code': '800.001.001', 'message': 'Failed to log action.'}
			kwargs = get_request_data(request)
			username = kwargs.pop("username")
			email = kwargs.pop("email")
			password = kwargs.pop("password")
			if username and not validate_name(username):
				self.mark_action_failed(action, code='999.002.006', description='Invalid Username')
				return {
					"code": "999.002.006", "message": "Username not valid", 'action_id': str(action.id)}
			
			if email and not validate_email(email):
				self.mark_action_failed(action, code='999.002.006', description='Invalid email')
				return {
					"code": "999.002.006", "message": "Email not valid", 'action_id': str(action.id)}
			
			if password and not validate_password(password):
				self.mark_action_failed(action, code='999.002.006', description='Password not valid')
				return {
					"code": "999.002.006", "message": "Password not valid", 'action_id': str(action.id)}
			
			user = UserService().create(username=username, email=email, password=password)
			group = GroupService().filter(name="Customers").first()
			if group is None:
				group = GroupService().create(name="Customers")
			user.groups.set(group)
			customer = CustomerService().create(user=user)
			if not customer:
				self.mark_action_failed(action, description="customer was not added", code="600.002.001")
				return {"code": "600.002.001", "message": "customer was not added.", "action_id": str(action.id)}
			self.complete_action(action, code='100.000.000', description='Success')
			return {'code': '100.000.000', 'message': 'Success', 'user': user}
		except Exception as e:
			self.mark_action_failed(action, description=str(e), code="999.999.999")
			return {
				"code": "999.999.999", "message": "Exception adding customer",
				"error": str(e), 'action': str(action.id)}

	def update_customer(self, request) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles updating of a customer
		@params request: Http request
		@type request: HttpRequest
		@params data: Key value object containing the data
		@type data: dict
		@return JsonResponse
		"""
		action = self.log_action(
			action_type="Edit customer", trace='backend/customer_base/update_customer', request=request)
		try:
			if not action:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			kwargs = get_request_data(request)
			customer_id = kwargs.get("customer")
			email = kwargs.pop("email")
			password = kwargs.pop("password")
			state_id = kwargs.get("state")
			
			if email and not validate_email(email):
				self.mark_action_failed(action, code='999.002.006', description='Invalid email')
				return {
					"code": "999.002.006", "message": "Email not valid", 'action_id': str(action.id)}
			
			if password and not validate_password(password):
				self.mark_action_failed(action, code='999.002.006', description='Password not valid')
				return {
					"code": "999.002.006", "message": "Password not valid", 'action_id': str(action.id)}

			if state_id:
				state = StateService().get(pk=state_id)
			to_update = {
				'email': email, 'passsword': password, 'state': state}
			data = {k: v for k, v in to_update.items() if v is not None}
			updated_customer = CustomerService().update(pk=customer_id, **data)
			if updated_customer < 1:
				self.mark_action_failed(
					action, code='600.002.007', description='customer failed to update')
				return {
					'code': '600.002.007', 'message': 'customer failed to update',
					'action': str(action.id)}
			serializer = CustomerSerializer(updated_customer)
			self.complete_action(action, code='100.000.000', description='Success')
			return {
				'code': '100.000.000', 'message': 'Success', 'data': serializer.data}
		except Exception as e:
			self.mark_action_failed(action, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error when updating loan customer',
				'action': str(action.id)}

	def get_all_customers(self, request) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles  reading of customers
		@params request: Http request
		@type request: HttpRequest
		@return JsonResponse
		@rtype JsonResponse with response code and data
		"""

		try:
			customers = CustomerService().filter()
			if not customers:
				return {
					'code': '600.002.404', 'message': 'customers not found'}
			serializer = CustomerSerializer(customers)
			return {
				'code': '100.000.000', 'message': 'Success', 'data': serializer.data}
		except Exception as e:
			return {"code": "999.999.999", "message": "Error fetching customers"}

	def get_customer(self, request) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles  reading of customers
		@params request: Http request
		@type request: HttpRequest
		@return JsonResponse
		@rtype JsonResponse with response code and data
		"""
		action = self.log_action(
			action_type="Get customer", trace='backend/customer_base/_customer', request=request)
		try:
			kwargs = get_request_data(request)
			customer_id = kwargs.pop("customer")
			if customer_id and not validate_uuid7(customer_id):
				self.mark_action_failed(action, code='999.005.006', description='Invalid customer')
				return {'code': '999.005.006', 'message': 'customer not valid', 'action': str(action.id)}
			customer = CustomerService().get(pk=customer_id)
			if not customer:
				self.mark_action_failed(action, description="customer not found", code="600.002.002")
				return {
					"code": "600.002.002", "message": "customer not found", 'action': str(action.id)}
			serializer = CustomerSerializer(customer)
			self.complete_action(action, description="customer  found", code="100.000.000")
			return {
				'code': '100.000.000', 'message': 'Success', 'data': serializer.data}
		except Exception as e:
			self.mark_action_failed(action, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error when fetching customer',
				'action': str(action.id)}

	def delete_customer(self, request):
		""" Mark customer as deleted """

		action = self.log_action(
			action_type="Delete customer", trace='backend/customer_base/delete_customer', request=request)
		try:
			kwargs = get_request_data(request)
			customer_id = kwargs.pop("customer")
			if customer_id and not validate_uuid7(customer_id):
				self.mark_action_failed(action, code='999.005.006', description='Invalid customer')
				return {'code': '999.005.006', 'message': 'customer not valid', 'action': str(action.id)}
			customer = CustomerService().get(pk=customer_id)
			if not customer:
				self.mark_action_failed(action, description="customer not found", code="600.002.002")
				return {
					"code": "600.002.002", "message": "customer not found", 'action': str(action.id)}
			deleted_state = StateService.get(name="deleted")
			CustomerService().update(pk=customer_id, status=deleted_state)
			self.mark_action_complete(action, description="customer  deleted", code="100.000.000")
			return {
				'code': '100.000.000', 'message': 'Success'}
		except Exception as e:
			self.mark_action_failed(action, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error when deleting customer',
				'action': str(action.id)}
