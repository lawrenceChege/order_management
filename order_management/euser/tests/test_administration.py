"""
Tests for Euser
"""
from django.db import transaction
from mixer.backend.django import mixer

from euser.administration.euser_administration import EUserAdministration
from euser.tests.test_setup import TestSetUp


class TestEuserAdministration(TestSetUp):
	"""
	Test for Euser Administration
	"""
	def test_add_custom_role(self):
		state = mixer.blend('base.State', name='Disabled')
		corporate = mixer.blend('corporate.Corporate')
		with transaction.atomic():
			k = {"name": "Some", 'corporate': str(corporate.id)}
			response = EUserAdministration().add_custom_role(request=None, **k)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Add Custom Role')
			k = {"name": "NA", 'corporate': str(corporate.id)}
			response = EUserAdministration().add_custom_role(request=None, **k)
			assert response.get('code') == '999.002.006', 'Should fail on invalid name'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Add Custom Role')
			k = {"name": "Some", 'corporate': "45w34dfffsdfvxcv"}
			response = EUserAdministration().add_custom_role(request=None, **k)
			assert response.get('code') == '300.001.002', 'Should fail on corporate not found'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Add Custom Role')
			k = {"name": "Some", 'corporate': str(corporate.id)}
			response = EUserAdministration().add_custom_role(request=None, **k)
			assert response.get('code') == '100.000.000', 'Should successfully add Custom Role'

	def test_disable_custom_role(self):
		state = mixer.blend('base.State', name='Disabled')
		role = mixer.blend('euser.Role', state=state)
		with transaction.atomic():
			data = {'role': str(role.id)}
			response = EUserAdministration().disable_custom_role(request=None, **data)
			assert response.get('code') == '800.001.001', 'Should fail to log transaction.'
		mixer.blend('base.TransactionType', name='Disable Custom Role')
		with transaction.atomic():
			data = {'role': str(role.id)}
			response = EUserAdministration().disable_custom_role(request=None, **data)
			assert response.get('code') == '100.000.000', 'Should successfully disable custom role'
		with transaction.atomic():
			data = {'role': '41c161c-53ad-48fb-9b52-1980b30b46e2'}
			response = EUserAdministration().disable_custom_role(request=None, **data)
			assert response.get('code') == '999.005.006', 'Should fail with invalid role message'

	def test_enable_custom_role(self):
		disabled = mixer.blend('base.State', name='Disabled')
		country = mixer.blend('base.Country', name='Kenya')
		region = mixer.blend('base.Region', name='Central', country=country)
		corporate = mixer.blend('corporate.Corporate', region=region)
		with transaction.atomic():
			data = {"corporate": str(corporate.id)}
			response = EUserAdministration().enable_custom_role(request=None, **data)
			assert response.get('code') == '800.001.001', 'Should fail to log transaction.'
		mixer.blend('base.TransactionType', name='Enable Custom Role')
		role = mixer.blend('euser.Role', state=disabled, corporate=corporate)
		with transaction.atomic():
			data = {'corporate': str(corporate.id), 'role': str(role.id)}
			response = EUserAdministration().enable_custom_role(request=None, **data)
			assert response.get('code') == '100.000.000', 'Should successfully enable custom role'
		role = mixer.blend('euser.Role', state=disabled)
		with transaction.atomic():
			data = {'corporate': str(corporate.id), 'role': str(role.id)}
			response = EUserAdministration().enable_custom_role(request=None, **data)
			assert response.get('code') == '500.005.002', 'Not a custom role'
		role = mixer.blend('euser.Role', corporate=corporate)
		with transaction.atomic():
			data = {'corporate': str(corporate.id), 'role': str(role.id)}
			response = EUserAdministration().enable_custom_role(request=None, **data)
			assert response.get('code') == '500.005.002', 'Disabled custom role not found'
		role = mixer.blend('euser.Role', state=disabled, corporate=corporate)
		with transaction.atomic():
			data = {'corporate': str(corporate.id)+'wer', 'role': str(role.id)}
			response = EUserAdministration().enable_custom_role(request=None, **data)
			assert response.get('code') == '999.005.006', 'Corporate not valid'
		role = mixer.blend('euser.Role', state=disabled, corporate=corporate)
		with transaction.atomic():
			data = {'corporate': '41c9161c-53ad-48fb-9b52-1980b30b46e2', 'role': str(role.id)}
			response = EUserAdministration().enable_custom_role(request=None, **data)
			assert response.get('code') == '300.001.002', 'Corporate not found'
		with transaction.atomic():
			data = {'corporate': str(corporate.id), 'role': '41c161c-53ad-48fb-9b52-1980b30b46e2'}
			response = EUserAdministration().enable_custom_role(request=None, **data)
			assert response.get('code') == '999.005.006', 'Role not valid'

	def test_add_custom_role_permission(self):
		role = mixer.blend('euser.Role', name='admin')
		permission = mixer.blend('euser.Permission',name='add user')
		with transaction.atomic():
			kwargs = {'role': role.id, 'permission': permission.id}
			resp = EUserAdministration().add_custom_role_permission(request=None, **kwargs)
			assert resp.get('code') == '800.001.001', "should fail, transaction not created"
		mixer.blend('base.TransactionType', name="Add Custom Role Permission")
		with transaction.atomic():
			kwargs = {'role': 'drhhjryjrukrkl', 'permission': permission.id}
			resp = EUserAdministration().add_custom_role_permission(request=None, **kwargs)
			assert resp.get('code') == '999.005.006', "Should fail, invalid role id"
		with transaction.atomic():
			kwargs = {'role': role.id, 'permission': 'rfgdrthhhiu'}
			resp = EUserAdministration().add_custom_role_permission(request=None, **kwargs)
			assert resp.get('code') == '999.006.006', "Should fail, invalid permission id"
		with transaction.atomic():
			kwargs = {'role': 'fba937de-9808-4313-a364-a8b9d0cda377', 'permission': permission.id}
			print(permission.id)
			resp = EUserAdministration().add_custom_role_permission(request=None, **kwargs)
			assert resp.get('code') == '500.005.001', "Should fail, Role not found"
		with transaction.atomic():
			kwargs = {'role': role.id, 'permission': role.id}
			resp = EUserAdministration().add_custom_role_permission(request=None, **kwargs)
			assert resp.get('code') == '500.006.001', "Should fail, permission not found"
		with transaction.atomic():
			kwargs = {'role': role.id, 'permission': permission.id}
			resp = EUserAdministration().add_custom_role_permission(request=None, **kwargs)
			assert resp.get('code') == '100.000.000', "Success"

	def test_enable_custom_role_permission(self):
		state = mixer.blend('base.State', name='Disabled')
		custom_role_permission = mixer.blend('euser.RolePermission', state=state)
		with transaction.atomic():
			k = {"custom_role_permission": str(custom_role_permission.id)}
			response = EUserAdministration().enable_custom_role_permission(request=None, **k)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Enable Custom Role Permission')
			k = {"custom_role_permission": str(custom_role_permission.id)}
			response = EUserAdministration().enable_custom_role_permission(request=None, **k)
			assert response.get('code') == '100.000.000', 'Should successfully enable Custom Role Permission'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Enable Custom Role Permission')
			k = {"custom_role_permission": str(state.id)}
			response = EUserAdministration().enable_custom_role_permission(request=None, **k)
			assert response.get('code') == '500.007.002', 'Should fail on missing Custom Role Permission'

	def test_disable_custom_role_permission(self):
		state = mixer.blend('base.State', name='Disabled')
		custom_role_permission = mixer.blend('euser.RolePermission', state=state)
		with transaction.atomic():
			k = {"custom_role_permission": str(custom_role_permission.id)}
			response = EUserAdministration().disable_custom_role_permission(request=None, **k)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Disable Custom Role Permission')
			k = {"custom_role_permission": str(custom_role_permission.id)}
			response = EUserAdministration().disable_custom_role_permission(request=None, **k)
			assert response.get('code') == '100.000.000', 'Should successfully enable Custom Role Permission'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Disable Custom Role Permission')
			k = {"custom_role_permission": "41c9161c-53ad-48fb-9b52-1980b30b46e2"}
			response = EUserAdministration().disable_custom_role_permission(request=None, **k)
			assert response.get('code') == '500.007.002', 'Should fail on missing Custom Role Permission'

	def test_add_organization_admin(self):
		branch = mixer.blend('corporate.Branch')
		mixer.blend('euser.Role', name="Admin")
		with transaction.atomic():
			data = {
				"branch": str(branch.id), "username": "Jebby",
				'email': 'jebby@gmail.com', 'phone_number': '0701234567'}
			response = EUserAdministration().add_organization_admin(request=None, **data)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		mixer.blend('base.TransactionType', name='Add Organization Admin')
		with transaction.atomic():
			data = {
				"branch": str(branch.id), "username": "Jebby",
				'email': 'jebby@gmail.com', 'phone_number': '070123a45670000'}
			response = EUserAdministration().add_organization_admin(request=None, **data)
			assert response.get('code') == '999.004.006', 'Should fail because of invalid phone'
		with transaction.atomic():
			data = {
				"branch": str(branch.id), "username": "Jebby", 'first_name': 'D',
				'email': 'jebby@gmail.com', 'phone_number': '0701234567'}
			response = EUserAdministration().add_organization_admin(request=None, **data)
			assert response.get('code') == '999.002.006', 'Should fail because of invalid first name'
		with transaction.atomic():
			data = {
				"branch": str(branch.id), "username": "Jebby", 'other_name': 'D',
				'email': 'jebby@gmail.com', 'phone_number': '0701234567'}
			response = EUserAdministration().add_organization_admin(request=None, **data)
			assert response.get('code') == '999.002.006', 'Should fail because of invalid other name'
		with transaction.atomic():
			data = {
				"branch": str(branch.id), "username": "Jebby", 'last_name': 'D',
				'email': 'jebby@gmail.com', 'phone_number': '0701234567'}
			response = EUserAdministration().add_organization_admin(request=None, **data)
			assert response.get('code') == '999.002.006', 'Should fail because of invalid last name'

		with transaction.atomic():
			data = {
				"branch": str(branch.id), "username": "Jebby",
				'email': 'jebby.gmail.com', 'phone_number': '0701234567'}
			response = EUserAdministration().add_organization_admin(request=None, **data)
			assert response.get('code') == '999.003.006', 'Should fail because of invalid email'

		with transaction.atomic():
			data = {
				"branch": str(branch.id), "username": "Jebby",
				'email': 'jebby@gmail.com', 'phone_number': '0701234567'}
			response = EUserAdministration().add_organization_admin(request=None, **data)
			assert response.get('code') == '100.000.000', 'Should be successful'

	def test_extended_user_permissions(self):
		corporate = mixer.blend('corporate.Corporate', name="New solution")
		branch=mixer.blend('corporate.Branch',name="Main",corporate=corporate)
		role= mixer.blend('euser.Role',name='Admin')
		user = mixer.blend('euser.Euser',branch=branch,role=role)
		permission = mixer.blend('euser.Permission')
		with transaction.atomic():
			k = {"user": str(user.id), 'permission': str(permission.id)}
			response = EUserAdministration().extend_user_permission(request=None, **k)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		mixer.blend('base.TransactionType', name="Extend User Permission")
		with transaction.atomic():
			k = {"user":'dfdgbhuygeygd', 'permission': str(permission.id)}
			response = EUserAdministration().extend_user_permission(request=None, **k)
			assert response.get('code') == '999.004.006', 'Should fail, invalid user'
		with transaction.atomic():
			k = {"user":'1ae03238-5738-49a4-99ca-c885e76c1081', 'permission': str(permission.id)}
			response = EUserAdministration().extend_user_permission(request=None, **k)
			assert response.get('code') == '500.004.002', 'Should fail, user not found'
		with transaction.atomic():
			k = {"user":str(user.id), 'permission': "dgfhhbddghhhg"}
			response = EUserAdministration().extend_user_permission(request=None, **k)
			assert response.get('code') == '999.006.006', 'Should fail, invalid permission'
		with transaction.atomic():
			k = {"user": str(user.id), 'permission': '1ae03238-5738-49a4-99ca-c885e76c1081'}
			response = EUserAdministration().extend_user_permission(request=None, **k)
			assert response.get('code') == '500.006.002', 'Should fail, user permission not found'
		with transaction.atomic():
			k = {"user": str(user.id), 'permission': permission.id}
			response = EUserAdministration().extend_user_permission(request=None, **k)
			assert response.get('code') == '100.000.000', 'Should successfully add permission to user'

	def test_add_organization_user(self):
		branch = mixer.blend('corporate.Branch')
		role = mixer.blend('euser.Role')
		user = mixer.blend('euser.EUser', role=role, branch=branch)
		with transaction.atomic():
			k = {"branch": str(branch.id), "other_name": "Some"}
			response = EUserAdministration().add_organization_user(request=None, **k)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Add Organization User')
			k = {"branch": str(branch.id), "role": str(role.id), "phone_number": "Some"}
			response = EUserAdministration().add_organization_user(request=None, **k)
			assert response.get('code') == '999.004.006', 'Should fail because of invalid phone'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Add Organization User')
			k = {"branch": str(branch.id), "role": str(role.id), "first_name": ""}
			response = EUserAdministration().add_organization_user(request=None, **k)
			assert response.get('code') == '999.002.006', 'Should fail because of invalid first name'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Add Organization User')
			k = {"branch": str(branch.id), "role": str(role.id), "email": "sijui.com"}
			response = EUserAdministration().add_organization_user(request=None, **k)
			assert response.get('code') == '999.003.006', 'Should fail because of invalid email'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Add Organization User')
			k = {
				"branch": str(branch.id), "role": str(role.id), "first_name": "Test", "last_name": "Some",
				"email": "mimi@sijui.com", "phone_number": "254777123456"}
			response = EUserAdministration().add_organization_user(request=None, **k)
			assert response.get('code') == '100.000.000', 'Should be successful'

	def test_support_user(self):
		branch = mixer.blend('corporate.Branch')
		mixer.blend('euser.Role', name="Support User")
		with transaction.atomic():
			k = {"branch": str(branch.id), "other_name": "Daisy"}
			response = EUserAdministration().add_support_user(request=None, **k)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		mixer.blend('base.TransactionType', name='Add Support User')
		with transaction.atomic():
			k = {"branch": str(branch.id), "phone_number": "None"}
			response = EUserAdministration().add_support_user(request=None, **k)
			assert response.get('code') == '999.004.006', 'Should fail because of invalid phone'
		with transaction.atomic():
			k = {"branch": str(branch.id), "first_name": ""}
			response = EUserAdministration().add_support_user(request=None, **k)
			assert response.get('code') == '999.002.006', 'Should fail because of invalid first name'
		with transaction.atomic():
			k = {"branch": str(branch.id), "email": "something.com"}
			response = EUserAdministration().add_support_user(request=None, **k)
			assert response.get('code') == '999.003.006', 'Should fail because of invalid email'
		with transaction.atomic():
			k = {
				"branch": str(branch.id), "first_name": "Test", "last_name": "Some",
				"email": "mimi@sijui.com", "phone_number": "254777123456"}
			response = EUserAdministration().add_support_user(request=None, **k)
			assert response.get('code') == '100.000.000', 'Should successfully create a support user'

	def test_update_organization_admin(self):
		role = mixer.blend('euser.Role', name="admin")
		corporate = mixer.blend('corporate.Corporate', name="Digi ltd")
		branch = mixer.blend('corporate.Branch', name="Main", corporate=corporate)
		euser = mixer.blend('euser.Euser', role=role, branch=branch)
		new_branch = mixer.blend('corporate.Branch', name="Nairobi Branch", corporate=corporate)
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'branch': new_branch.id}
			response = EUserAdministration().update_organization_admin(request=None, **k)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		mixer.blend('base.TransactionType', name="Update Organization Admin")
		with transaction.atomic():
			k = {'user': 'dfdghbfbhdhg', 'first_name': "John", 'email': 'John@doe.com', 'branch': new_branch.id}
			response = EUserAdministration().update_organization_admin(request=None, **k)
			assert response.get('code') == '999.005.006', 'should fail invalid user  provided'
		with transaction.atomic():
			k = {'user': str(role.id), 'first_name': "John", 'email': 'John@doe.com', 'branch': new_branch.id}
			response = EUserAdministration().update_organization_admin(request=None, **k)
			assert response.get('code') == '500.004.002', 'should fail user not found'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'branch': 'erftygdg'}
			response = EUserAdministration().update_organization_admin(request=None, **k)
			assert response.get('code') == '999.005.006', 'should fail, invalid branch'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'branch': str(role.id)}
			response = EUserAdministration().update_organization_admin(request=None, **k)
			assert response.get('code') == '500.002.002', 'should fail, branch not found'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'phone_number': '254stdbe'}
			response = EUserAdministration().update_organization_admin(request=None, **k)
			assert response.get('code') == '999.004.006', 'should fail, invalid phone number'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'Jdoe.com'}
			response = EUserAdministration().update_organization_admin(request=None, **k)
			assert response.get('code') == '999.003.006', 'should fail, invalid phone number'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'branch': new_branch.id}
			response = EUserAdministration().update_organization_admin(request=None, **k)
			assert response.get('code') == '100.000.000'

	def test_update_organization_user(self):
		role = mixer.blend('euser.Role', name="admin")
		corporate = mixer.blend('corporate.Corporate', name="Digi ltd")
		branch = mixer.blend('corporate.Branch', name="Main", corporate=corporate)
		euser = mixer.blend('euser.Euser', role=role, branch=branch)
		new_branch = mixer.blend('corporate.Branch', name="Nairobi Branch", corporate=corporate)
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'branch': new_branch.id}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		mixer.blend('base.TransactionType', name="Update Organization User")
		with transaction.atomic():
			k = {'user': 'dfdghbfbhdhg', 'first_name': "John", 'email': 'John@doe.com', 'branch': new_branch.id}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '999.005.006', 'should fail invalid user  provided'
		with transaction.atomic():
			k = {'user': str(role.id), 'first_name': "John", 'email': 'John@doe.com', 'branch': new_branch.id}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '500.004.002', 'should fail user not found'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'branch': 'erftygdg'}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '999.005.006', 'should fail, invalid branch'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'branch': str(role.id)}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '500.002.002', 'should fail, branch not found'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'role': 'erftygdg'}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '999.005.006', 'should fail, invalid role'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'role': str(branch.id)}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '500.005.002', 'should fail, role not found'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'phone_number': '254stdbe'}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '999.004.006', 'should fail, invalid phone number'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'Jdoe.com'}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '999.003.006', 'should fail, invalid phone number'
		with transaction.atomic():
			k = {'user': euser.id, 'first_name': "John", 'email': 'John@doe.com', 'branch': new_branch.id}
			response = EUserAdministration().update_organization_user(request=None, **k)
			assert response.get('code') == '100.000.000'

	def test_update_support_user(self):
		branch = mixer.blend('corporate.Branch')
		role = mixer.blend('euser.Role')
		user = mixer.blend('euser.EUser', role=role, branch=branch)
		with transaction.atomic():
			k = {"euser": str(user.id), "other_name": "Some"}
			response = EUserAdministration().update_support_user(request=None, **k)
			assert response.get('code') == '800.001.001', 'Should fail because of missing Transaction Type'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Update Support User')
			k = {"euser": str(user.id), "phone_number": "Some"}
			response = EUserAdministration().update_support_user(request=None, **k)
			assert response.get('code') == '999.004.006', 'Should fail because of invalid phone'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Update Support User')
			k = {"euser": str(user.id), "first_name": ""}
			response = EUserAdministration().update_support_user(request=None, **k)
			assert response.get('code') == '999.002.006', 'Should fail because of invalid first name'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Update Support User')
			k = {"euser": str(user.id), "email": "sijui.com"}
			response = EUserAdministration().update_support_user(request=None, **k)
			assert response.get('code') == '999.003.006', 'Should fail because of invalid email'
		with transaction.atomic():
			mixer.blend('base.TransactionType', name='Update Support User')
			k = {"euser": str(user.id), "email": "mimi@sijui.com"}
			response = EUserAdministration().update_support_user(request=None, **k)
			assert response.get('code') == '100.000.000', 'Should be successful'

	def test_get_user(self):
		"""
		This method for testing get a corporate administration
		"""
		# state = mixer.blend('base.State', name="Active")
		state = mixer.blend('base.State',name='New state')
		corporate = mixer.blend('corporate.Corporate',name="new ltd")
		role = mixer.blend('euser.Role',name="Admin")
		branch = mixer.blend('corporate.Branch', name="Main",corporate=corporate)
		add_branch = mixer.blend('euser.Permission',name="add branch")
		add_user = mixer.blend('euser.Permission',name="add user")
		euser = mixer.blend('euser.EUser',first_name="James", last_name="peter", branch=branch, role=role)
		mixer.blend('euser.ExtendedEUserPermission',euser=euser,permission=add_user)
		mixer.blend('euser.ExtendedEUserPermission',euser=euser,permission=add_branch)
		with transaction.atomic():
			kwargs = {'user': euser.id}
			resp = EUserAdministration().get_user(request=None, **kwargs)
			assert resp.get('code') == '800.001.001', "Should fail because of missing Transaction Type"
		mixer.blend('base.TransactionType', name='Get User')
		with transaction.atomic():
			kwargs = {'user': "dgffjghhb"}
			resp = EUserAdministration().get_user(request=None, **kwargs)
			assert resp.get('code') == '999.005.006', "Should fail, invalid user"
		with transaction.atomic():
			kwargs = {'user': str(role.id)}
			resp = EUserAdministration().get_user(request=None, **kwargs)
			assert resp.get('code') == '500.004.002', "Should fail, user not found"
		with transaction.atomic():
			k = {'user': str(euser.id)}
			print("k %s" %k)
			resp = EUserAdministration().get_user(request=None, **k)
			assert resp.get('code') == '100.000.000', "Success"

	def test_disable_user(self):
		disabled = mixer.blend('base.State', name='Disabled')
		country = mixer.blend('base.Country', name='Kenya')
		region = mixer.blend('base.Region', name='Central', country=country)
		corporate = mixer.blend('corporate.Corporate', region=region)
		branch = mixer.blend('corporate.Branch', name="main", corporate=corporate)
		role = mixer.blend('euser.Role', name="Approve")
		permissions = mixer.blend('euser.Permission', name="Add user")
		user = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		with transaction.atomic():
			data = {"euser": str(user.id)}
			response = EUserAdministration().disable_user(request=None, **data)
			assert response.get('code') == '800.001.001', 'Should fail to log transaction.'
		mixer.blend('base.TransactionType', name='Disable User')
		user = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		with transaction.atomic():
			data = {"euser": str(user.id)}
			response = EUserAdministration().disable_user(request=None, **data)
			assert response.get('code') == '100.000.000', 'Successfully disabled user'
		with transaction.atomic():
			data = {"euser": '41c9161c-53ad-48fb-9b52-1980b30bas46e2'}
			response = EUserAdministration().disable_user(request=None, **data)
			assert response.get('code') == '999.005.006', 'Euser not valid'
		user = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		with transaction.atomic():
			data = {"euser": '41c9161c-53ad-48fb-9b52-1980b30b46e2'}
			response = EUserAdministration().disable_user(request=None, **data)
			assert response.get('code') == '500.004.002', 'User not found'

	def test_enable_user(self):
		state = mixer.blend('base.State', name='Disabled')
		corporate = mixer.blend('corporate.Corporate')
		branch = mixer.blend('corporate.Branch', name="main", corporate=corporate)
		role = mixer.blend('euser.Role', name="Approve")
		permissions = mixer.blend('euser.Permission', name="Add user")
		user = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		with transaction.atomic():
			data = {"euser": str(user.id)}
			response = EUserAdministration().enable_user(request=None, **data)
			assert response.get('code') == '800.001.001', 'Should fail to log transaction.'
		mixer.blend('base.TransactionType', name='Enable User')
		user = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions,state=state)
		with transaction.atomic():
			data = {"euser": str(user.id)}
			response = EUserAdministration().enable_user(request=None, **data)
			assert response.get('code') == '100.000.000', 'Successfully enable user'
		with transaction.atomic():
			data = {"euser": '41c9161c-53ad-48fb-9b52-1980b30bas46e2'}
			response = EUserAdministration().enable_user(request=None, **data)
			assert response.get('code') == '999.005.006', 'Euser not valid'
		with transaction.atomic():
			data = {"euser": '41c9161c-53ad-48fb-9b52-1980b30b46e2'}
			response = EUserAdministration().enable_user(request=None, **data)
			assert response.get('code') == '500.004.002', 'User not found'

