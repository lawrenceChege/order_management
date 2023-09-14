import pytest
from mixer.backend.django import mixer

from euser.backend.services import RoleService, PermissionService, RolePermissionService, EUserPasswordService, \
	EUserService, ExtendedEUserPermissionService
from euser.tests.test_setup import TestSetUp

pytestmark = pytest.mark.django_db


class TestRoleService(TestSetUp):
	"""
	Test the Role Model Services
	"""

	def test_get(self):
		"""
		Test Role get service
		"""
		role = mixer.blend('euser.Role', name="Admin")
		role_new = RoleService().get(name="Admin")
		assert role_new is not None, 'Should have an Role object'
		assert role_new.name == role.name, 'Should return Admin as name'

	def test_filter(self):
		"""
		Test Role filter service
		"""
		mixer.cycle(3).blend('euser.Role', state=self.state_approval_pending)
		roles = RoleService().filter(state=self.state_approval_pending)
		assert len(roles) == 3, 'Should have 3 Role objects'

	def test_create(self):
		"""
		Test Role create service
		"""
		role = RoleService().create(name="Loan Officer", state=self.state_approval_pending)
		assert role is not None, 'Should have an Role object'
		assert role.name == 'Loan Officer', 'Should return Loan officer as Name'

	def test_update(self):
		"""
		Test Role update service
		"""
		role = mixer.blend('euser.Role',state = self.state_active)
		updated_role = RoleService().update(role.id, name="Loan Officer")
		assert updated_role is not None, 'Should have an Role object'
		assert updated_role.name == 'Loan Officer', 'Should return Loan officer as Name'


class TestPermissionService(TestSetUp):
	"""
	Test the Permission Model Services
	"""

	def test_get(self):
		"""
		Test Permission get service
		"""
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		permission_new = PermissionService().get(state=self.state_active)
		assert permission_new is not None, 'Should have an Permission object'
		assert permission_new.name == permission.name, 'Should return approve loan as name'

	def test_filter(self):
		"""
		Test Permission filter service
		"""
		mixer.cycle(3).blend('euser.Permission', state=self.state_active)
		perm = PermissionService().filter(state=self.state_active)
		assert len(perm) == 3, 'Should have 3 Permission objects'

	def test_create(self):
		"""
		Test Permission create service
		"""
		perm = PermissionService().create(name="approve loan", state=self.state_active)
		assert perm is not None, 'Should have an Permission object'
		assert perm.name == 'approve loan', 'Should return approve loan as Name'

	def test_update(self):
		"""
		Test Permission update service
		"""
		perm = mixer.blend('euser.Permission',state=self.state_active)
		updated_perm = PermissionService().update(perm.id, name="initiate loan")
		assert updated_perm is not None, 'Should have an Permission object'
		assert updated_perm.name == 'initiate loan', 'Should return initiate loan as Name'


class TestRolePermissionService(TestSetUp):
	"""
	Test the RolePermission Model Services
	"""

	def test_get(self):
		"""
		Test RolePermission get service
		"""
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		role_permission = mixer.blend('euser.RolePermission', state=self.state_active, role=role, permission=permission)
		role_permission_new = RolePermissionService().get(state=self.state_active)
		assert role_permission_new is not None, 'Should have an RolePermission object'
		assert role_permission_new.role == role, 'Should return role'

	def test_filter(self):
		"""
		Test RolePermission filter service
		"""
		mixer.blend('euser.Role', state=self.state_active)
		mixer.blend('euser.Permission', state=self.state_active)
		mixer.cycle(3).blend('euser.RolePermission', state=self.state_active)
		perm = RolePermissionService().filter(state=self.state_active)
		assert len(perm) == 3, 'Should have 3 RolePermission objects'

	def test_create(self):
		"""
		Test RolePermission create service
		"""
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		perm = RolePermissionService().create(state=self.state_active, role=role, permission=permission)
		assert perm is not None, 'Should have an RolePermission object'
		assert perm.permission == permission, 'Should return a permission object'

	def test_update(self):
		"""
		Test RolePermission update service
		"""
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		perm = mixer.blend('euser.RolePermission')
		updated_perm = RolePermissionService().update(perm.id, permission=permission)
		assert updated_perm is not None, 'Should have an RolePermission object'
		assert updated_perm.permission == permission, 'Should return a permission object'


class TestEUserPasswordService(TestSetUp):
	"""
	Test the EUserPassword Model Services
	"""

	def test_get(self):
		"""
		Test EUserPassword get service
		"""
		branch = mixer.blend('corporate.Branch')
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		e_user = mixer.blend('euser.EUser', state=self.state_active, role=role, permission=permission, branch=branch)
		e_pass = mixer.blend('euser.EUserPassword', state=self.state_active, euser=e_user)
		e_pass_new = EUserPasswordService().get(state=self.state_active)
		assert e_pass_new is not None, 'Should have an EUserPassword object'
		assert e_pass_new.euser == e_pass.euser, 'Should return euser'

	def test_filter(self):
		"""
		Test EUserPassword filter service
		"""
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		branch = mixer.blend('corporate.Branch')
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		euser = mixer.blend('euser.EUser', state=self.state_active, role=role, permission=permission, branch=branch)
		mixer.cycle(3).blend('euser.EUserPassword', state=self.state_active, euser=euser)
		perm = EUserPasswordService().filter(state=self.state_active)
		assert len(perm) == 3, 'Should have 3 EUserPassword objects'

	def test_create(self):
		"""
		Test EUserPassword create service
		"""

		branch = mixer.blend('corporate.Branch',state=self.state_active)
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		euser = mixer.blend('euser.EUser', state=self.state_active, role=role, permission=permission, branch=branch)
		e_pass = EUserPasswordService().create(state=self.state_active, euser=euser)
		assert e_pass is not None, 'Should have an EUserPassword object'
		assert e_pass.euser == euser, 'Should return a euser object'

	def test_update(self):
		"""
		Test EUserPassword update service
		"""

		branch = mixer.blend('corporate.Branch',state=self.state_active)
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		euser = mixer.blend('euser.EUser', state=self.state_active, role=role, permission=permission, branch=branch)
		e_pass = mixer.blend('euser.EUserPassword', euser=euser)
		updated_e_pass = EUserPasswordService().update(e_pass.id, euser=euser)
		assert updated_e_pass is not None, 'Should have an EUserPassword object'
		assert updated_e_pass.euser == euser, 'Should return a euser object'


class TestEUserService(TestSetUp):
	"""
	Test the EUser Model Services
	"""

	def test_get(self):
		"""
		Test EUser get service
		"""
		branch = mixer.blend('corporate.Branch',state=self.state_active)
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		e_user = mixer.blend('euser.EUser', state=self.state_active, role=role, permissions=permission, branch=branch)
		e_user_new = EUserService().get(pk=e_user.id)
		assert e_user_new is not None, 'Should have an EUser object'
		assert e_user_new.role == e_user.role, 'Should return role'

	def test_filter(self):
		"""
		Test EUser filter service
		"""
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		branch = mixer.blend('corporate.Branch')
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		mixer.cycle(3).blend('euser.EUser', state=self.state_active, role=role, permissions=permission, branch=branch)
		perm = EUserService().filter(state=self.state_active)
		assert len(perm) == 3, 'Should have 3 EUser objects'

	def test_create(self):
		"""
		Test EUser create service
		"""
		branch = mixer.blend('corporate.Branch',state=self.state_active)
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		e_user = EUserService().create(state=self.state_active, role=role, branch=branch)
		assert e_user is not None, 'Should have an EUser object'
		assert e_user.role == role, 'Should return a role object'

	def test_update(self):
		"""
		Test EUser update service
		"""

		branch = mixer.blend('corporate.Branch',state=self.state_active)
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		euser = mixer.blend('euser.EUser', state=self.state_active, role=role, permissions=permission, branch=branch)
		updated_e_pass = EUserService().update(euser.id, first_name="Karen")
		assert updated_e_pass is not None, 'Should have an EUser object'
		assert updated_e_pass.first_name == "Karen", 'Should return a euser object'


class TestExtendedEUserPermissionService(TestSetUp):
	"""
	Test the ExtendedEUserPermission Model Services
	"""

	def test_get(self):
		"""
		Test ExtendedEUserPermission get service
		"""
		branch = mixer.blend('corporate.Branch',state=self.state_active)
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		e_user = mixer.blend('euser.EUser', state=self.state_active, role=role, branch=branch)
		ex_perm = mixer.blend('euser.ExtendedEUserPermission', euser=e_user, state=self.state_active)
		e_user_new = ExtendedEUserPermissionService().get(state=self.state_active)
		assert e_user_new is not None, 'Should have an ExtendedEUserPermission object'
		assert e_user_new.permission == ex_perm.permission, 'Should return permission'

	def test_filter(self):
		"""
		Test ExtendedEUserPermission filter service
		"""
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		branch = mixer.blend('corporate.Branch')
		euser = mixer.blend('euser.EUser', state=self.state_active, role=role, branch=branch)
		mixer.cycle(3).blend('euser.ExtendedEUserPermission', euser=euser, state=self.state_active)
		perm = ExtendedEUserPermissionService().filter(state=self.state_active)
		assert len(perm) == 3, 'Should have 3 ExtendedEUserPermission objects'

	def test_create(self):
		"""
		Test ExtendedEUserPermission create service
		"""

		branch = mixer.blend('corporate.Branch', state=self.state_active)
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		euser = mixer.blend('euser.EUser', state=self.state_active, role=role, branch=branch)
		ex_perm = ExtendedEUserPermissionService().create(euser=euser, permission=permission, state=self.state_active)
		assert ex_perm is not None, 'Should have an ExtendedEUserPermission object'
		assert ex_perm.permission == permission, 'Should return a permission object'

	def test_update(self):
		"""
		Test ExtendedEUserPermission update service
		"""
		branch = mixer.blend('corporate.Branch',state=self.state_active)
		role = mixer.blend('euser.Role', name="Admin", state=self.state_active)
		permission = mixer.blend('euser.Permission', name="approve loan", state=self.state_active)
		euser = mixer.blend('euser.EUser', state=self.state_active, role=role, permissions=permission, branch=branch)
		ex_perm = mixer.blend('euser.ExtendedEUserPermission', euser=euser)
		ex_perm_update = ExtendedEUserPermissionService().update(pk=ex_perm.id, state=self.state_active)
		assert ex_perm_update is not None, 'Should have an ExtendedEUserPermission object'
		assert ex_perm_update.state == self.state_active, 'Should return a permission object'
