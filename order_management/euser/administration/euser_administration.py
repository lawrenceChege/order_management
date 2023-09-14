"""
This module will hold administration for Euser
"""
from itertools import chain

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from audit.administration.audit_administration import TransactionLogBase
from base.backend.services import StateService
from base.backend.utils.validators import validate_uuid4, validate_name, validate_phone_number, validate_email, \
	normalize_phone_number
from corporate.backend.services import CorporateService, BranchService
from euser.backend.services import RoleService, EUserService, ExtendedEUserPermissionService, PermissionService, \
	RolePermissionService


class EUserAdministration(TransactionLogBase):
	"""
	Administration for Euser
	"""

	def add_custom_role(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles adding of custom role
		@params request: Http request
		@type request: HttpRequest
		@params kwargs: Key value object containing the data
		@type kwargs: dict
		@return JsonResponse
		"""
		# TODO: Amend after merging Lawrence work on corporate part of role model. Also check meta: Unique together
		transaction = self.log_transaction(
			transaction_type="Add Custom Role", trace='euser/add_custom_role', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			k = {}
			name = kwargs.pop("name")
			corporate = kwargs.pop("corporate")
			if not validate_name(name, 3):
				self.mark_transaction_failed(transaction, code="999.002.006", description="Invalid name")
				return {"code": "999.002.006", "message": "Invalid name", "transaction": str(transaction.id)}
			k['name'] = name
			corporate = CorporateService().get(pk=corporate)
			if not corporate:
				self.mark_transaction_failed(transaction, code="300.001.002", description="Corporate not found.")
				return {"code": "300.001.002", "message": "Corporate not found.", "transaction": str(transaction.id)}
			k['corporate'] = corporate
			k['is_corporate_role'] = True
			role = RoleService().create(**k)
			if not role:
				self.mark_transaction_failed(transaction, code="500.005.001", description="Role not added")
				return {"code": "500.005.001", "message": "Role not added", "transaction": str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'role': str(role.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {'code': '999.999.999', 'message': 'Error adding custom role', 'transaction': str(transaction.id)}

	def disable_custom_role(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		The method disables custom role in an organization
		@param request: The http request object
		@type request: HttpRequest
		@param kwargs: Key - Value arguments
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Disable Custom Role", trace='euser/disable_custom_role', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			role_id = kwargs.get('role')
			if role_id and not validate_uuid4(role_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid role')
				return {'code': '999.005.006', 'message': 'Invalid role', 'transaction': str(transaction.id)}
			role = RoleService().get(pk=role_id)
			if not role:
				self.mark_transaction_failed(transaction, code='500.005.002', description='Custom role not found')
				return {'code': '500.005.002', 'message': 'Custom role not found', 'transaction': str(transaction.id)}
			disabled = StateService().get(name="Disabled")
			role = RoleService().update(pk=role_id, state=disabled)
			if role:
				self.complete_transaction(transaction, "100.000.000", "Success")
				return {'code': '100.000.000', 'message': 'Success', 'data': {'role': str(role.id)}}
			self.mark_transaction_failed(transaction, code="300.001.001", description='Failed to disable custom role.')
			return {
				'code': '500.005.001', 'message': 'Failed to disable custom role.', 'transaction': str(transaction.id)}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {'code': '999.999.999', 'message': 'Error disabling custom role', 'transaction': str(transaction.id)}

	def enable_custom_role(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		The method enables custom role in an organization
		@param request: The http request object
		@type request: HttpRequest
		@param kwargs: Key - Value arguments
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Enable Custom Role", trace='euser/enable_custom_role', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			role_id = kwargs.get('role')
			corporate_id = kwargs.get('corporate')
			if corporate_id and not validate_uuid4(corporate_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid Corporate')
				return {'code': '999.005.006', 'message': 'Corporate not valid', 'transaction': str(transaction.id)}
			corporate = CorporateService().get(pk=corporate_id)
			if not corporate:
				self.mark_transaction_failed(transaction, code='300.001.002', description='Corporate not found')
				return {'code': '300.001.002', 'message': 'Corporate not found', 'transaction': str(transaction.id)}
			if role_id and not validate_uuid4(role_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid Role')
				return {'code': '999.005.006', 'message': 'Role not valid', 'transaction': str(transaction.id)}
			disabled = StateService().get(name="Disabled")
			role = RoleService().get(pk=role_id, corporate=corporate, state=disabled)
			if not role:
				self.mark_transaction_failed(
					transaction, code='500.005.002', description='Disabled custom role not found')
				return {
					'code': '500.005.002', 'message': 'Disabled custom role not found',
					'transaction': str(transaction.id)}
			active = StateService().get(name="Active")
			role = RoleService().update(pk=role_id, state=active)
			if role:
				self.complete_transaction(transaction, "100.000.000", "Success")
				return {'code': '100.000.000', 'message': 'Success', 'data': {'corporate': str(role.id)}}
			self.mark_transaction_failed(transaction, code="500.005.007", description='Failed to enable  custom role.')
			return {
				'code': '500.005.007', 'message': 'Failed to enable custom role.', 'transaction': str(transaction.id)}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return JsonResponse({
				'code': '999.999.999', 'message': 'Error when enabling custom role',
				'transaction': str(transaction.id)})

	def add_custom_role_permission(
			self, request, **data) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		This method handles adding of custom role permission
		@params request: Http request
		@type request: HttpRequest
		@params data: Key value object containing the data
		@type data: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Add Custom Role Permission", trace='euser/add_custom_role_permission',
			request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			role = data.pop('role')
			permission = data.pop('permission')
			k = {}
			if role and not validate_uuid4(role):
				self.mark_transaction_failed(transaction, code="999.005.006", description="Invalid role")
				return {"code": "999.005.006", "message": "Invalid role", "transaction": str(transaction.id)}
			role = RoleService().get(pk=role)
			if not role:
				self.mark_transaction_failed(transaction, code="500.005.001", description="Role not found")
				return {"code": "500.005.001", "message": "Permission not found", "transaction": str(transaction.id)}
			k['role'] = role
			if permission and not validate_uuid4(permission):
				self.mark_transaction_failed(transaction, code="999.005.006", description="Invalid permission")
				return {"code": "999.006.006", "message": "Invalid permission", "transaction": str(transaction.id)}
			permission = PermissionService().get(pk=permission)
			if not permission:
				self.mark_transaction_failed(transaction, code="500.006.001", description="Permission not found")
				return {"code": "500.006.001", "message": "Permission not found", "transaction": str(transaction.id)}
			k['permission'] = permission
			role_permission = RolePermissionService().create(**k)
			if not role_permission:
				self.mark_transaction_failed(transaction, code="500.007.001", description="Role permission not found")
				return {
					"code": "500.007.001", "message": "Role permission not found", "transaction": str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'role_permission': str(role_permission.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return JsonResponse({
				'code': '999.999.999', 'message': 'Error adding custom role permission',
				'transaction': str(transaction.id)})

	def enable_custom_role_permission(
			self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Enable Custom Role Permission
		:param request: HTTPRequest
		:param kwargs: Dict
		:return: JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Enable Custom Role Permission", trace='euser/enable_custom_role_permission',
			request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			custom_role_permission = kwargs.pop('custom_role_permission')
			active = StateService().get(name="Active")
			disabled = StateService().get(name="Disabled")
			custom_role_permission = RolePermissionService().get(id=custom_role_permission, state=disabled)
			if not custom_role_permission:
				self.mark_transaction_failed(
					transaction, code="500.007.002", description='Custom Role Permission not found.')
				return {
					'code': '500.007.002', 'message': 'Custom Role Permission not found.',
					'transaction': str(transaction.id)}
			custom_role_permission = RolePermissionService().update(pk=custom_role_permission.id, state=active)
			if custom_role_permission:
				self.complete_transaction(transaction, "100.000.000", "Success")
				return {
					'code': '100.000.000', 'message': 'Success',
					'data': {'custom_role_permission': str(custom_role_permission.id)}}
			self.mark_transaction_failed(
				transaction, code="500.007.001", description='Failed to enable custom role permission.')
			return {
				'code': '500.007.001', 'message': 'Failed to enable custom role permission.',
				'transaction': str(transaction.id)}
		except Exception as e:
			self.mark_transaction_failed(transaction, code="999.999.999", description=str(e))
			return {
				"code": "999.999.999", 'message': "Error enabling custom role permission.",
				'transaction': str(transaction.id)}

	def disable_custom_role_permission(
			self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Disable Custom Role Permission
		:param request: HTTPRequest
		:param kwargs: Dict
		:return: JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Disable Custom Role Permission", trace='euser/disable_custom_role_permission',
			request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			custom_role_permission = kwargs.pop('custom_role_permission')
			custom_role_permission = RolePermissionService().get(id=custom_role_permission)
			if not custom_role_permission:
				self.mark_transaction_failed(
					transaction, code="500.007.002", description='Custom Role Permission not found.')
				return {
					'code': '500.007.002', 'message': 'Custom Role Permission not found.',
					'transaction': str(transaction.id)}
			disabled = StateService().get(name="Disabled")
			custom_role_permission = RolePermissionService().update(pk=custom_role_permission.id, state=disabled)
			if custom_role_permission:
				self.complete_transaction(transaction, "100.000.000", "Success")
				return {
					'code': '100.000.000', 'message': 'Success',
					'data': {'custom_role_permission': str(custom_role_permission.id)}}
			self.mark_transaction_failed(
				transaction, code="500.007.001", description='Failed to disable custom role permission.')
			return {
				'code': '500.007.001', 'message': 'Failed to disable custom role permission.',
				'transaction': str(transaction.id)}
		except Exception as e:
			self.mark_transaction_failed(transaction, code="999.999.999", description=str(e))
			return {
				"code": "999.999.999", 'message': "Error disabling custom role permission.",
				'transaction': str(transaction.id)}

	def add_organization_admin(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		The method adds an organization admin
		@param request: The http request object
		@type request: HttpRequest
		@param kwargs: Key - Value arguments
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Add Organization Admin", trace='euser/enable_custom_role', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			branch_id = kwargs.pop('branch')
			username = kwargs.pop('username')
			first_name = kwargs.get('first_name')
			last_name = kwargs.get('last_name')
			other_name = kwargs.get('other_name')
			phone_number = kwargs.pop('phone_number')
			email = kwargs.pop('email')
			if branch_id and not validate_uuid4(branch_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid Branch')
				return {'code': '999.005.006', 'message': 'Branch not valid', 'transaction': str(transaction.id)}
			branch = BranchService().get(pk=branch_id)
			if username and not validate_name(username):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid username')
				return {'code': '999.002.006', 'message': 'Username is invalid.', 'transaction': str(transaction.id)}
			if first_name and not validate_name(str(first_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid first name')
				return {'code': '999.002.006', 'message': 'First name is invalid.', 'transaction': str(transaction.id)}
			if other_name and not validate_name(str(other_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid other name')
				return {'code': '999.002.006', 'message': 'Other name is invalid.', 'transaction': str(transaction.id)}
			if last_name and not validate_name(str(last_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid last name')
				return {'code': '999.002.006', 'message': 'last name is invalid.', 'transaction': str(transaction.id)}
			if phone_number and not validate_phone_number(phone_number):
				self.mark_transaction_failed(transaction, code='999.004.006', description='Invalid phone number')
				return {
					'code': '999.004.006', 'message': 'Phone number is invalid. Use format 0712345678',
					'transaction': str(transaction.id)}
			phone_number = normalize_phone_number(phone_number)
			if email and not validate_email(email):
				self.mark_transaction_failed(transaction, code='999.003.006', description='Invalid email')
				return {
					'code': '999.003.006', 'message': 'Email is invalid. Use format someone@somecompany.something',
					'transaction': str(transaction.id)}

			role = RoleService().get(name='Admin')
			if not role:
				self.mark_transaction_failed(transaction, code='500.005.002', description='Admin role not found')
				return {'code': '500.005.002', 'message': 'Admin role not found', 'transaction': str(transaction.id)}

			organizational_admin = EUserService().create(
				branch=branch, username=username, first_name=first_name, last_name=last_name, other_name=other_name,
				phone_number=phone_number, email=email, role=role)
			if not organizational_admin:
				self.mark_transaction_failed(
					transaction, code='500.007.001', description='Failed to add organization admin')
				return {
					'code': '500.007.001', 'message': 'Failed to add organization admin',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'role': str(organizational_admin.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return JsonResponse({
				'code': '999.999.999', 'message': 'Error when adding organization admin',
				'transaction': str(transaction.id)})

	def extend_user_permission(self, request, **data) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Extend user permission
		:param request: HTTPRequest
		:param data: Dict
		:return: JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Extend User Permission", trace='euser/extend_user_permission', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			user = data.pop('user')
			permission = data.pop('permission')
			k = {}
			if user and not validate_uuid4(user):
				self.mark_transaction_failed(
					transaction, code="999.004.006", description='Invalid user.')
				return {'code': '999.004.006', 'message': 'Invalid user.', 'transaction': str(transaction.id)}
			euser = EUserService().get(pk=user)
			if not euser:
				self.mark_transaction_failed(transaction, code="500.004.002", description='User not found.')
				return {'code': '500.004.002', 'message': 'User not found.', 'transaction': str(transaction.id)}
			k['euser'] = euser
			if permission and not validate_uuid4(permission):
				self.mark_transaction_failed(transaction, code="500.006.006", description='Invalid permission.')
				return {'code': '999.006.006', 'message': 'Invalid permission.', 'transaction': str(transaction.id)}
			permission = PermissionService().get(pk=permission)
			if not permission:
				self.mark_transaction_failed(transaction, code="500.006.002", description='Permission not found.')
				return {'code': '500.006.002', 'message': 'Permission not found.', 'transaction': str(transaction.id)}
			k['permission'] = permission
			extend_user_permission = ExtendedEUserPermissionService().create(**k)
			if not extend_user_permission:
				self.mark_transaction_failed(
					transaction, code="500.003.002", description='Extend user permission not added.')
				return {
					'code': '500.003.002', 'message': 'Extend user permission not added.',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, code='100.000.000', description='Success', )
			return {'code': '100.000.000', 'message': 'Success', 'data': str(extend_user_permission.id)}
		except Exception as e:
			self.mark_transaction_failed(transaction, code="999.999.999", description=str(e))
			return {
				"code": "999.999.999", 'message': "Error extending user permission.",
				'transaction': str(transaction.id)}

	def add_organization_user(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Add Organization User.
		:param request: HTTPRequest
		:param kwargs: Dict
		:return: JsonResponse
		"""
		# TODO: Support staff differentiators?
		transaction = self.log_transaction(
			transaction_type="Add Organization User", trace='euser/add_organization_user', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			branch = kwargs.pop("branch")
			role = kwargs.pop("role")
			first_name = kwargs.get("first_name")
			last_name = kwargs.get("last_name")
			other_name = kwargs.get("other_name")
			phone_number = kwargs.get("phone_number")
			email = kwargs.get("email")
			language_code = kwargs.get("language_code", "en")
			k = {}
			if phone_number:
				if not validate_phone_number(normalize_phone_number(phone_number)):
					self.mark_transaction_failed(transaction, code='999.004.006', description='Invalid phone number')
					return {
						'code': '999.004.006', 'message': 'Invalid phone number', 'transaction_id': str(transaction.id)}
				k['phone_number'] = normalize_phone_number(phone_number)
			k['first_name'] = str(first_name).strip().title()
			if not validate_name(str(first_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid first name')
				return {'code': '999.002.006', 'message': 'Invalid first name', 'transaction_id': str(transaction.id)}
			k['first_name'] = str(first_name).strip().title()
			if not validate_name(str(last_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid last name')
				return {'code': '999.002.006', 'message': 'Invalid last name', 'transaction_id': str(transaction.id)}
			k['last_name'] = str(last_name).strip().title()
			if other_name:
				if not validate_name(str(other_name)):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid other name')
					return {
						'code': '999.002.006', 'message': 'Invalid other name', 'transaction_id': str(transaction.id)}
				k['other_name'] = str(other_name).strip().title()
			if not validate_email(str(email)):
				self.mark_transaction_failed(transaction, code='999.003.006', description='Invalid email')
				return {
					'code': '999.003.006', 'transaction_id': str(transaction.id),
					'message': 'Email is invalid. Provide email in format someone@somecompany.something'}
			k['email'] = str(email).strip().lower()
			k['language_code'] = language_code
			branch = BranchService().get(pk=branch)
			if not branch:
				self.mark_transaction_failed(transaction, code='300.002.002', description='Branch not found')
				return {'code': '300.002.002', 'message': 'Branch not found', 'transaction_id': str(transaction.id)}
			k['branch'] = branch
			role = RoleService().get(pk=role)
			if not role:
				self.mark_transaction_failed(transaction, code='500.005.002', description='Role not found')
				return {'code': '500.005.002', 'message': 'Role not found', 'transaction_id': str(transaction.id)}
			k['role'] = role
			user = EUserService().create(**k)
			if not user:
				self.mark_transaction_failed(transaction, code="500.007.001", description='Failed to add user.')
				return {'code': '500.007.001', 'message': 'Failed to add user.', 'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'user': str(user.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code="999.999.999", description=str(e))
			return {"code": "999.999.999", 'message': "Error adding user", 'transaction': str(transaction.id)}

	def add_support_user(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Add support user.
		:param request: HTTPRequest
		:param kwargs: Dict
		:return: JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Add Support User", trace='euser/add_support_user', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			branch = kwargs.pop("branch")
			first_name = kwargs.get("first_name")
			last_name = kwargs.get("last_name")
			other_name = kwargs.get("other_name")
			phone_number = kwargs.get("phone_number")
			email = kwargs.get("email")
			language_code = kwargs.get("language_code", "en")
			k = {}
			if phone_number:
				if not validate_phone_number(normalize_phone_number(phone_number)):
					self.mark_transaction_failed(transaction, code='999.004.006', description='Invalid phone number')
					return {
						'code': '999.004.006', 'message': 'Invalid phone number', 'transaction_id': str(transaction.id)}
				k['phone_number'] = normalize_phone_number(phone_number)
			k['first_name'] = str(first_name).strip().title()
			if not validate_name(str(first_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid first name')
				return {'code': '999.002.006', 'message': 'Invalid first name', 'transaction_id': str(transaction.id)}
			k['first_name'] = str(first_name).strip().title()
			if not validate_name(str(last_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid last name')
				return {'code': '999.002.006', 'message': 'Invalid last name', 'transaction_id': str(transaction.id)}
			k['last_name'] = str(last_name).strip().title()
			if other_name:
				if not validate_name(str(other_name)):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid other name')
					return {
						'code': '999.002.006', 'message': 'Invalid other name', 'transaction_id': str(transaction.id)}
				k['other_name'] = str(other_name).strip().title()
			if not validate_email(str(email)):
				self.mark_transaction_failed(transaction, code='999.003.006', description='Invalid email')
				return {
					'code': '999.003.006', 'transaction_id': str(transaction.id),
					'message': 'Email is invalid. Provide email in format someone@somecompany.something'}
			k['email'] = str(email).strip().lower()
			k['language_code'] = language_code
			branch = BranchService().get(pk=branch)
			if not branch:
				self.mark_transaction_failed(transaction, code='300.002.002', description='Branch not found')
				return {'code': '300.002.002', 'message': 'Branch not found', 'transaction_id': str(transaction.id)}
			k['branch'] = branch
			role = RoleService().get(name="Support User")
			if not role:
				self.mark_transaction_failed(transaction, code='500.005.002', description='Role not found')
				return {'code': '500.005.002', 'message': 'Role not found', 'transaction_id': str(transaction.id)}
			k['role'] = role
			user = EUserService().create(**k)
			if not user:
				self.mark_transaction_failed(transaction, code="500.007.001", description='Failed to add support user.')
				return {
					'code': '500.007.001', 'message': 'Failed to add support user.', 'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'user': str(user.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code="999.999.999", description=str(e))
			return {"code": "999.999.999", 'message': "Error adding support user", 'transaction': str(transaction.id)}

	def update_organization_admin(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		The method updates an organization admin
		@param request: The http request object
		@type request: HttpRequest
		@param kwargs: Key - Value arguments
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Update Organization Admin", trace='euser/update_organization_admin', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			org_admin_id = kwargs.pop('user')
			branch = kwargs.get('branch')
			username = kwargs.get('username')
			first_name = kwargs.get('first_name')
			last_name = kwargs.get('last_name')
			other_name = kwargs.get('other_name')
			phone_number = kwargs.get('phone_number')
			email = kwargs.get('email')
			k = {}
			if not validate_uuid4(org_admin_id):
				self.mark_transaction_failed(transaction, code="999.005.006", description="Invalid user")
				return {"code": "999.005.006", "message": "Invalid user", "transaction": str(transaction.id)}
			euser = EUserService().get(pk=org_admin_id)
			if not euser:
				self.mark_transaction_failed(transaction, code="500.004.002", description="User not found")
				return {"code": "500.004.002", "message": "User not found", "transaction": str(transaction.id)}
			if branch:
				if not validate_uuid4(branch):
					self.mark_transaction_failed(transaction, code="999.005.006", description="Invalid branch")
					return {"code": "999.005.006", "message": "Invalid branch", "transaction": str(transaction.id)}
				branch = BranchService().get(pk=branch)
				if not branch:
					self.mark_transaction_failed(transaction, code="500.002.002", description="Branch not found")
					return {"code": "500.002.002", "message": "Branch not found", "transaction": str(transaction.id)}
				k['branch'] = branch
			if username:
				if not validate_name(username):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid username')
					return {
						'code': '999.002.006', 'message': 'Username is invalid.', 'transaction': str(transaction.id)}
				k['user_name'] = username
			if first_name:
				if not validate_name(str(first_name)):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid first name')
					return {
						'code': '999.002.006', 'message': 'First name is invalid.',	'transaction': str(transaction.id)}
				k['first_name'] = first_name
			if other_name:
				if not validate_name(str(other_name)):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid other name')
					return {
						'code': '999.002.006', 'message': 'Other name is invalid.',	'transaction': str(transaction.id)}
				k['other_name'] = str(other_name).strip().title()
			if last_name:
				if not validate_name(str(last_name)):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid last name')
					return {
						'code': '999.002.006', 'message': 'last name is invalid.',	'transaction': str(transaction.id)}
				k['last_name'] = str(last_name).strip().title()
			if phone_number:
				if not validate_phone_number(normalize_phone_number(phone_number)):
					self.mark_transaction_failed(transaction, code='999.004.006', description='Invalid phone number')
					return {
						'code': '999.004.006', 'message': 'Phone number is invalid. Use format 254712345678',
						'transaction': str(transaction.id)}
				k['phone_number'] = phone_number
			if email:
				if not validate_email(email):
					self.mark_transaction_failed(transaction, code='999.003.006', description='Invalid email')
					return {
						'code': '999.003.006', 'message': 'Email is invalid. Use format someone@somecompany.something',
						'transaction': str(transaction.id)}
				k['email'] = email
			update_organizational_admin = EUserService().update(org_admin_id, **k)
			if not update_organizational_admin:
				self.mark_transaction_failed(
					transaction, code='500.007.007', description='Failed to update organization admin')
				return {
					'code': '500.007.001', 'message': 'Failed to update organization admin',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'role': str(update_organizational_admin.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error updating organization admin',
				'transaction': str(transaction.id)}

	def update_organization_user(self, request, **data) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Update Organization User
		:param request: HTTPRequest
		:param data: Dict
		:return: JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Update Organization User", trace='euser/enable_custom_role_permission',
			request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			branch = data.get('branch')
			role = data.get('role')
			first_name = data.get('first_name')
			last_name = data.get('last_name')
			other_name = data.get('other_name')
			phone_number = data.get('phone_number')
			email = data.get('email')
			user = data.pop('user')
			k = {}
			if not validate_uuid4(user):
				self.mark_transaction_failed(transaction, code="999.005.006", description="Invalid user")
				return {"code": "999.005.006", "message": "Invalid user", "transaction": str(transaction.id)}
			euser = EUserService().get(pk=user)
			if not euser:
				self.mark_transaction_failed(transaction, code="500.004.002", description="User not found")
				return {"code": "500.004.002", "message": "User not found", "transaction": str(transaction.id)}
			if branch:
				if not validate_uuid4(branch):
					self.mark_transaction_failed(transaction, code="999.005.006", description="Invalid branch")
					return {"code": "999.005.006", "message": "Invalid branch", "transaction": str(transaction.id)}
				branch = BranchService().get(pk=branch)
				if not branch:
					self.mark_transaction_failed(transaction, code="500.002.002", description="Branch not found")
					return {"code": "500.002.002", "message": "Branch not found", "transaction": str(transaction.id)}
				k['branch'] = branch
			if role:
				if not validate_uuid4(role):
					self.mark_transaction_failed(transaction, code="999.005.006", description="Invalid role")
					return {"code": "999.005.006", "message": "Invalid role", "transaction": str(transaction.id)}
				role = RoleService().get(pk=role)
				if not role:
					self.mark_transaction_failed(transaction, code="500.005.002", description="Role not found")
					return {"code": "500.005.002", "message": "Role not found", "transaction": str(transaction.id)}
				k['role'] = role
			if phone_number:
				phone_number = normalize_phone_number(phone_number)
				if not validate_phone_number(phone_number):
					self.mark_transaction_failed(transaction, code="999.004.006", description="Invalid phone number")
					return {
						"code": "999.004.006", "message": "Invalid phone number", "transaction": str(transaction.id)}
				k['phone_number'] = phone_number
			if email:
				if not validate_email(email):
					self.mark_transaction_failed(
						transaction, code="999.003.006",
						description="Invalid email, provide email in format you@someone.me")
					return {
						"code": "999.003.006", "message": "Invalid email, provide email in format you@someone.me",
						"transaction": str(transaction.id)}
				k['email'] = email
			if first_name:
				if not validate_name(str(first_name), 2):
					self.mark_transaction_failed(transaction, code="999.002.006", description="Invalid first name")
					return {"code": "500.002.006", "message": "Invalid first name", "transaction": str(transaction.id)}
				k['first_name'] = str(first_name).strip().title()
			if last_name:
				if not validate_name(str(last_name), 2):
					self.mark_transaction_failed(transaction, code="999.002.006", description="Invalid last name")
					return {"code": "500.002.006", "message": "Invalid last name", "transaction": str(transaction.id)}
				k['last_name'] = str(last_name).strip().title()
			if other_name:
				if not validate_name(str(other_name), 2):
					self.mark_transaction_failed(transaction, code="999.002.006", description="Invalid other name")
					return {"code": "500.002.006", "message": "Invalid other name", "transaction": str(transaction.id)}
				k['other_name'] = str(other_name).strip().title()
			euser = EUserService().update(euser.id, **k)
			if not euser:
				self.mark_transaction_failed(transaction, code="500.004.002", description="User not updated")
				return {"code": "500.004.002", "message": "User not updated", "transaction": str(transaction.id)}
			self.complete_transaction(transaction, code='100.000.000', description='Success')
			return {"code": "100.000.000", "me": "Success"}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {'code': '999.999.999', 'message': 'Error updating user', 'transaction': str(transaction.id)}

	def update_support_user(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Update support user.
		:param request: HTTPRequest
		:param kwargs: Dict
		:return: JsonResponse
		"""
		# TODO: Support staff differentiators?
		transaction = self.log_transaction(
			transaction_type="Update Support User", trace='euser/update_support_user', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			euser = kwargs.pop("euser")
			first_name = kwargs.get("first_name")
			last_name = kwargs.get("last_name")
			other_name = kwargs.get("other_name")
			phone_number = kwargs.get("phone_number")
			email = kwargs.get("email")
			language_code = kwargs.get("language_code", "en")
			k = {}
			if phone_number:
				if not validate_phone_number(normalize_phone_number(phone_number)):
					self.mark_transaction_failed(transaction, code='999.004.006', description='Invalid phone number')
					return {
						'code': '999.004.006', 'message': 'Invalid phone number', 'transaction_id': str(transaction.id)}
				k['phone_number'] = normalize_phone_number(phone_number)
			k['first_name'] = str(first_name).strip().title()
			if not validate_name(str(first_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid first name')
				return {'code': '999.002.006', 'message': 'Invalid first name', 'transaction_id': str(transaction.id)}
			k['first_name'] = str(first_name).strip().title()
			if not validate_name(str(last_name)):
				self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid last name')
				return {'code': '999.002.006', 'message': 'Invalid last name', 'transaction_id': str(transaction.id)}
			k['last_name'] = str(last_name).strip().title()
			if other_name:
				if not validate_name(str(other_name)):
					self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid other name')
					return {
						'code': '999.002.006', 'message': 'Invalid other name', 'transaction_id': str(transaction.id)}
				k['other_name'] = str(other_name).strip().title()
			if not validate_email(str(email)):
				self.mark_transaction_failed(transaction, code='999.003.006', description='Invalid email')
				return {
					'code': '999.003.006', 'transaction_id': str(transaction.id),
					'message': 'Email is invalid. Provide email in format someone@somecompany.something'}
			k['email'] = str(email).strip().lower()
			k['language_code'] = language_code
			user = EUserService().update(pk=euser, **k)
			if not user:
				self.mark_transaction_failed(
					transaction, code="500.007.001", description='Failed to update support staff.')
				return {
					'code': '500.007.001', 'message': 'Failed to update support staff.',
					'transaction': str(transaction.id)}
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Success', 'data': {'user': str(user.id)}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code="999.999.999", description=str(e))
			return {
				"code": "999.999.999", 'message': "Error updating support staff.", 'transaction': str(transaction.id)}

	def get_user(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		Get user.
		:param request: HTTPRequest
		:param kwargs: Dict
		:return: JsonResponse
		"""
		transaction = self.log_transaction(transaction_type="Get User", trace='euser/get_user', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			user = kwargs.get('user')
			if not validate_uuid4(user):
				self.mark_transaction_failed(transaction, code="999.005.006", description='Invalid user.')
				return {'code': '999.005.006', 'message': 'Invalid user.', 'transaction': str(transaction.id)}
			euser = EUserService().get(pk=user)
			if not euser:
				self.mark_transaction_failed(transaction, code="500.004.002", description="User not found")
				return {"code": "500.004.002", "message": "User not found ", "transaction": str(transaction.id)}
			extended_permissions = list(ExtendedEUserPermissionService().filter(
				euser=euser, state__name='Active').values_list('permission__id', flat=True))
			print(extended_permissions)
			role_permissions = list(RolePermissionService().filter(
				role=euser.role, state__name='Active').values_list('permission__id', flat=True))
			permissions = list(chain(extended_permissions, role_permissions))
			data = {
				"first_name": euser.first_name, "last_name": euser.last_name, "phone_number": euser.phone_number,
				"email": euser.email, "branch": {"branch_id":str(euser.branch.id),"name":euser.branch.name},
				'role':{"role_id":str(euser.role.id),"name":euser.role.name},
				'permissions':list(permissions)}
			self.complete_transaction(transaction, code="100.000.000", description="Success")
			return {"code": "100.000.000", "message": "Success", 'data': {'user': data}}
		except Exception as e:
			self.mark_transaction_failed(transaction, code="999.999.999", description=str(e))
			return {"code": "999.999.999", 'message': "Error fetching  user.", 'transaction': str(transaction.id)}

	def disable_user(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		The method enables custom role in and organization
		@param request: The http request object
		@type request: HttpRequest
		@param kwargs: Key - Value arguments
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Disable User", trace='euser/disable', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			user_id = kwargs.get('euser')
			if user_id and not validate_uuid4(user_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid User')
				return {'code': '999.005.006', 'message': 'Euser not valid', 'transaction': str(transaction.id)}
			active = StateService().get(name="Active")
			user = EUserService().get(pk=user_id, state=active)
			if not user:
				self.mark_transaction_failed(transaction, code='500.004.002', description='User not found')
				return {'code': '500.004.002', 'message': 'User not found', 'transaction': str(transaction.id)}
			disabled = StateService().get(name="Disabled")
			user = EUserService().update(pk=user_id, state=disabled)
			if user:
				self.complete_transaction(transaction, "100.000.000", "Success")
				return {'code': '100.000.000', 'message': 'Success', 'data': {'user': str(user.id)}}
			self.mark_transaction_failed(transaction, code="300.001.001", description='Failed to disable user.')
			return {'code': '500.004.001', 'message': 'Failed to disable user', 'transaction': str(transaction.id)}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return JsonResponse({
				'code': '999.999.999', 'message': 'Error when disabling user', 'transaction': str(transaction.id)})

	def enable_user(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		The method enables a user
		@param request: The http request object
		@type request: HttpRequest
		@param kwargs: Key - Value arguments
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Enable User", trace='euser/enable_user', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			user_id = kwargs.get('euser')
			if user_id and not validate_uuid4(user_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid User')
				return {'code': '999.005.006', 'message': 'Euser not valid', 'transaction': str(transaction.id)}
			disabled = StateService().get(name="Disabled")
			user = EUserService().get(pk=user_id, state=disabled)
			if not user:
				self.mark_transaction_failed(transaction, code='500.004.002', description='EUser not found')
				return {'code': '500.004.002', 'message': 'EUser not found', 'transaction': str(transaction.id)}
			active = StateService().get(name="Active")
			user = EUserService().update(pk=user_id, state=active)
			if user:
				self.complete_transaction(transaction, "100.000.000", "Success")
				return {'code': '100.000.000', 'message': 'Success', 'data': {'user': str(user.id)}}
			self.mark_transaction_failed(transaction, code="300.001.001", description='Failed to enable user.')
			return {'code': '500.004.001', 'message': 'Failed to enable user', 'transaction': str(transaction.id)}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error enabling user', 'transaction': str(transaction.id)}

	def change_password(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
		"""
		handles changing of user password
		@param request: The http request object
		@type request: HttpRequest
		@param kwargs: Key - Value arguments
		@type kwargs: dict
		@return JsonResponse
		"""
		transaction = self.log_transaction(
			transaction_type="Change Password", trace='euser/change_password', request=request)
		try:
			if not transaction:
				return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
			new_password = kwargs.get('new_password')
			current_password = kwargs.get('current_password')
			user_id = kwargs.get('user')
			active = StateService().get(name="Active")
			if user_id and not validate_uuid4(user_id):
				self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid User')
				return {'code': '999.005.006', 'message': 'User is not valid', 'transaction': str(transaction.id)}
			e_user = EUserService().get(pk=user_id, state=active)
			if not e_user:
				self.mark_transaction_failed(transaction, code='500.004.002', description='EUser not found')
				return {'code': '500.004.002', 'message': 'User not found', 'transaction': str(transaction.id)}
			if not e_user.check_password(current_password):
				self.mark_transaction_failed(transaction, code="500.004.006", description='Old password is incorrect')
				return {'code': '500.004.006', "message": "Old password is incorrect"}
			if e_user.check_password(new_password):
				self.mark_transaction_failed(
					transaction, code="500.004.003", description='New password cannot be same as old password')
				return {'code': '500.004.003', "message": "New password cannot be same as old password"}
			e_user.set_password(new_password)
			self.complete_transaction(transaction, "100.000.000", "Success")
			return {'code': '100.000.000', 'message': 'Password successfully changed'}
		except Exception as e:
			self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
			return {
				'code': '999.999.999', 'message': 'Error changing user ', 'transaction': str(transaction.id)}
