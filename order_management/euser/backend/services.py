"""
euser module services
"""
from base.backend.servicebase import ServiceBase
from euser.models import EUser, EUserPassword, Role, Permission, RolePermission, ExtendedEUserPermission, \
	EUserSecurityQuestion


class RoleService(ServiceBase):
	"""
	This class handles all the CRUD operations for the Role Model
	"""

	manager = Role.objects


class PermissionService(ServiceBase):
	"""
	This class handles all the CRUD operations for the Permission Model
	"""
	manager = Permission.objects


class RolePermissionService(ServiceBase):
	"""
	This class handles all the CRUD operations for the RolePermission Model
	"""
	manager = RolePermission.objects


class EUserPasswordService(ServiceBase):
	"""
	This class handles all the CRUD operations for the EUserPassword Model
	"""
	manager = EUserPassword.objects


class EUserSecurityQuestionService(ServiceBase):
	"""
	This class handles all the CRUD operations for the EUserSecurityQuestion Model
	"""
	manager = EUserSecurityQuestion.objects


class EUserService(ServiceBase):
	"""
	This class handles all the CRUD operations for the EUser Model.
	"""
	manager = EUser.objects


class ExtendedEUserPermissionService(ServiceBase):
	"""
	This class handles all the CRUD operations for the ExtendedUserPermission Model
	"""
	manager = ExtendedEUserPermission.objects
