from unittest import TestCase

import pytest
from mixer.backend.django import mixer

from base.models import BaseModel
from euser.models import AbstractEUser, EUser

pytestmark = pytest.mark.django_db


class TestUsersModels:
	"""
		This class tests all the the Euser module models.
		Should return a model instance for a pass nad None for a fail
	"""

	def test_role(self):
		"""
			This method tests the Role model and will return a Role instance if successful
			or None if not
			:return: Role | None
			:rtype: Object

		"""
		obj = mixer.blend('euser.Role', name="Approve")
		assert obj is not None, 'Should create roles instance'
		assert obj.__str__() == '%s' % obj.name, 'Should return string representation of Role instance '
		assert obj.__repr__() == 'Role_name=Approve,Is_corporate_role=False,Is_service_provider_role=False,' \
								 'Is_super_admin=False', 'should return repr of role '

	def test_roles_with_no_name(self):
		"""
			Test for role model with no name
		"""
		with pytest.raises(Exception) as e:
			obj = mixer.blend('euser.Role', name=None)
		assert "IntegrityError" in str(e)

	def test_permission(self):
		"""
			This method tests the Permission model and will return a Role instance if successful
			or None if not
			:return: Permission | None
			:rtype: Object
		"""
		state = mixer.blend('base.State', name="Active")
		obj = mixer.blend('euser.Permission', name='Add user', simple_name="can add user")
		assert obj is not None, 'should create instance of permission'
		assert obj.__str__() == "%s" % obj.name, 'should return string instance of object Permissions'
		assert obj.__repr__() == 'Permission_name = Add user,simple_name = can add user'

	def test_Permission_invalid_input(self):
		"""
			this method test Permission model on invalid input it should raise and exception
			:return: Exception
			:rtype: Exception of type DoesNotExist
		"""
		with pytest.raises(Exception) as e:
			obj = mixer.blend('euser.Permission', state="Disabled")
		assert "DoesNotExist" in str(e)

	def test_role_permissions(self):
		"""
			This method tests the RolePermission model and returns a RolePermission instance
			if successful or None if Failed
			:return: RolePermission | None
			:rtype: Object
		"""
		state = mixer.blend('base.State', name="Active")
		obj = mixer.blend('euser.RolePermission')
		assert obj is not None, 'Should create instance of role permission'
		assert obj.__str__() == '%s %s' % (obj.role.name, obj.permission.name)

	def test_euser_security_question(self):
		"""
			This method tests the UserSecurityQuestion model and returns a UserSecurityQuestion instance if success
			:return: UserSecurityQuestion | None
			:rtype: Object
		"""

		state = mixer.blend('base.State', name="Active")
		corporate = mixer.blend('corporate.Corporate', name="Tai sacco", state=state)
		branch = mixer.blend('corporate.Branch', name="main", corporate=corporate)
		role = mixer.blend('euser.Role', name="Approve")
		permissions = mixer.blend('euser.Permission', name="Add user")
		euser = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		obj = mixer.blend('euser.EUserSecurityQuestion', euser=euser)
		assert obj is not None, 'Should return instance of security question model'
		assert obj.__str__() == "%s %s %s" % (obj.euser, obj.security_question, obj.state)

	def test_euser(self):
		"""
			this test creation of user in euser model
		"""
		state = mixer.blend('base.State', name="Active")
		corporate = mixer.blend('corporate.Corporate', name="Tai sacco", state=state)
		branch = mixer.blend('corporate.Branch', name="main", corporate=corporate)
		role = mixer.blend('euser.Role', name="Approve")
		permissions = mixer.blend('euser.Permission', name="Add user")
		obj = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		assert obj is not None, 'Should return instance of EUser model'
		assert obj.__str__() == "%s %s - %s" % (obj.branch, obj.username, obj.role)

	def test_extended_euser_permissions(self):
		"""
			This method tests the ExtendedUserPermission model and returns an ExtendedUserPermission if successful and None if not
			:return: ExtendedUserPermission | None
			:rtype: Object
		"""
		state = mixer.blend('base.State', name="Active")
		corporate = mixer.blend('corporate.Corporate', name="Tai sacco", state=state)
		branch = mixer.blend('corporate.Branch', name="main", corporate=corporate)
		role = mixer.blend('euser.Role', name="Approve")
		permissions = mixer.blend('euser.Permission', name="Add user")
		permission = mixer.blend('euser.Permission', name="Add customer")
		euser = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		obj = mixer.blend('euser.ExtendedEUserPermission', euser=euser, permission=permission)
		assert obj is not None, 'Should return instance of ExtendedEUserPermission model'
		assert obj.__str__() == "%s %s" % (obj.euser, obj.permission.name)

	def test_role_permission(self):
		"""
			test for role perission mapping model (roleperemission model)

		"""
		state = mixer.blend('base.State', name="Active")
		role = mixer.blend('euser.Role', name="Approve")
		permissions = mixer.blend('euser.Permission', name="Add user")
		obj = mixer.blend('euser.RolePermission', role=role, permission=permissions)
		assert obj is not None, 'Should return instance of RolePermission model'
		assert obj.__str__() == "%s %s" % (obj.role.name, obj.permission.name)
		assert obj.__repr__() == 'role_name = Approve, permission_name=Add user'

	def test_euser_password(self):
		"""
			test for user credentials
		"""
		state = mixer.blend('base.State', name="Active")
		corporate = mixer.blend('corporate.Corporate', name="Tai sacco", state=state)
		branch = mixer.blend('corporate.Branch', name="main", corporate=corporate)
		role = mixer.blend('euser.Role', name="Approve")
		permissions = mixer.blend('euser.Permission', name="Add user")
		euser = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		obj = mixer.blend('euser.EUserPassword', euser=euser)
		assert obj is not None, 'Should return instance of EuserPassword model'
		assert obj.__str__() == "%s" % obj.password


class TestAbstractEUser(object):
	""" Test abstract e user"""

	def test_get_full_name(self):
		"""
			Tests the get full name raises abstract model cannot be instantiated  exception.
		"""
		with pytest.raises(Exception) as e:
			AbstractEUser().get_full_name()
		assert 'TypeError' in str(e), "Should  fail on direct call"

	def test_get_short_name(self):
		"""
			Tests the get full name raises abstract model cannot be instantiated  exception.
		"""
		with pytest.raises(Exception) as e:
			AbstractEUser().get_short_name()
		assert 'TypeError' in str(e), "Should  fail on direct call"

	def test_get_session_auth_hash(self):
		"""
		Test the get session auth hash method
		:return: salted_hmac password
		"""
		state = mixer.blend('base.State', name="Active")
		assert EUser(BaseModel, AbstractEUser).get_session_auth_hash() is not None, 'Should return hashed password.'

	def test_get_email_field_name(self):
		"""
			Test the get email field name method.
		"""
		try:
			state = mixer.blend('base.State', name="Active")
			assert AbstractEUser.get_email_field_name() is None, 'Should return email field name as None.'
		except Exception as e:
			raise e

	def test_normalize_username(self):
		"""
			Test the get username field method.
		"""
		state = mixer.blend('base.State', name="Active")
		corporate = mixer.blend('corporate.Corporate', name="Tai sacco", state=state)
		branch = mixer.blend('corporate.Branch', name="main", corporate=corporate)
		role = mixer.blend('euser.Role', name="Approve")
		permissions = mixer.blend('euser.Permission', name="Add user")
		euser = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		assert AbstractEUser.normalize_username(euser.username) is not None, 'Should return username field name.'

	def test_user_return_username(self):
		state = mixer.blend('base.State', name="Active")
		corporate = mixer.blend('corporate.Corporate', name="Tai sacco", state=state)
		branch = mixer.blend('corporate.Branch', name="main", corporate=corporate)
		role = mixer.blend('euser.Role', name="Approve")
		permissions = mixer.blend('euser.Permission', name="Add user")
		euser = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
		assert AbstractEUser.get_username(euser) == "%s" % euser.username, 'Should return username field name.'

	def test_user_return_password(self):
		try:
			state = mixer.blend('base.State', name="Active")
			assert EUser(BaseModel, AbstractEUser).password is not None, 'Should return hashed password.'
		except Exception as e:
			raise e

	def test_security_questions(self):
			state = mixer.blend('base.State', name="Active")
			corporate = mixer.blend('corporate.Corporate', name="Tai sacco", state=state)
			branch = mixer.blend('corporate.Branch', name="main", corporate=corporate)
			role = mixer.blend('euser.Role', name="Approve")
			permissions = mixer.blend('euser.Permission', name="Add user")
			user = mixer.blend('euser.EUser', branch=branch, role=role, permissions=permissions)
			assert user.security_questions is not None, 'should return set of security questions.'


class TestEUserModelsReturnedObject(TestCase):
	"""
	This class test whether the returned objects matches the ones declared on model creation
	"""

	def test_returned_objects(self):
		state = mixer.blend('base.State', name='Active')
		user = mixer.blend('euser.EUser', state=state, is_superuser=True)
		expected_obj = 'None %s - None' % user.username
		self.assertEqual(expected_obj, str(user)), 'username should match'
		# User helper functions
		user.clean()  # Clean the username
		assert isinstance(user.natural_key(), tuple), 'Should be the username tuple'
		assert user.get_full_name() is not None, 'Should be the names string'
		assert user.get_short_name() is not None, 'Should be the username string'
		assert user.get_all_permissions() is not None, 'Should successfully retrieve some permissions for the user'
		assert user.is_anonymous is not None, 'Should be Callable False'
		assert user.get_username() is not None, 'Should return password'
		assert user.get_username().__str__() == "%s" % user.username, 'should return match for password'
		assert user.is_authenticated is not None, 'Should be Callable True'
		assert user.password is None, 'Should find no password at all'
		user.set_unusable_password()  # Set unusable password.
		assert user.has_usable_password() is True, 'Should get no usable password'
		assert user.get_group_permissions() is not None, 'Should get some group permissions'
		assert user.has_perm('tester') is not None, 'Should check if the user has the permission'
		user.is_active = True
		user.is_superuser = True
		assert user.has_perms(['tester']) is not None, 'Should check if the user has the permission'
		assert user.has_module_perms('tester') is True, 'Should check if the user has permissions if super user'
		user.is_superuser = False
		user.branch = mixer.blend('corporate.Branch')
		user.role = mixer.blend('euser.Role')
		user = mixer.blend('euser.EUser', state=state, is_superuser=True)
		assert user.has_module_perms('tester') is not None, 'Should check if the user has permissions'
		user.set_password('ab12563')
		user.save()  # Save for testing save
		assert user.password is not None, 'should return  password'

		user_pass_obj = mixer.blend('euser.EUserPassword', euser=user, state=state)
		expected_obj = '%s' % user_pass_obj.password
		self.assertEqual(str(expected_obj), str(user_pass_obj)), 'user password check if password match'
		assert isinstance(str(user_pass_obj), str), \
			'Should successfully retrieve the unicode for the model'

		role_obj = mixer.blend('euser.Role', state=state)
		expected_obj = '%s' % role_obj.name
		self.assertEqual(str(expected_obj), str(role_obj))

		permission_obj = mixer.blend('euser.Permission', state=state)
		expected_obj = '%s' % permission_obj.name
		self.assertEqual(str(expected_obj), str(permission_obj)), 'should check if user has permission'

		role_permission_obj = mixer.blend(
			'euser.RolePermission', role=role_obj,
			permission=permission_obj, state=state)
		expected_obj = '%s %s' % (
			role_permission_obj.role.name, role_permission_obj.permission.name)
		self.assertEqual(str(expected_obj), str(role_permission_obj)), 'should return role permission'
		ext_user_perm_obj = mixer.blend(
			'euser.ExtendedEUserPermission', euser=user,
			permission=permission_obj, state=state)
		expected_obj = '%s %s' % (ext_user_perm_obj.euser, ext_user_perm_obj.permission.name)
		self.assertEqual(str(expected_obj), str(ext_user_perm_obj)), 'should return Extended Euser permision '

		user_sec_question = mixer.blend(
			'euser.EUserSecurityQuestion', euser=user, state=state)
		expected_obj = '%s %s %s' % (
			user_sec_question.euser, user_sec_question.security_question.name, user_sec_question.state)
		self.assertEqual(str(expected_obj), str(user_sec_question)), 'should return security  question'
