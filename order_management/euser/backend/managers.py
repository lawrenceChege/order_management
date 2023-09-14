"""
The model managers.
"""
from django.contrib.auth.base_user import BaseUserManager


class EUserManager(BaseUserManager):
	"""
	The E user manager
	"""
	use_in_migrations = True

	def _create_user(self, username, password, **extra_fields):
		"""
		Creates and saves an EUser with the given email and password.
		"""
		if not username:
			raise ValueError('The username for the e user must be set')

		user = self.model(username = username, **extra_fields)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_user(self, username, password = None, **extra_fields):
		"""Wrapper for creating a user"""
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(username, password, **extra_fields)

	def create_superuser(self, username, password, **extra_fields):
		"""Wrapper for creating a super user"""
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_staff', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(username, password, **extra_fields)
