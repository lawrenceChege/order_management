"""
	This file holds serializers for models in the EUser module.
	Converts Model Objects into JSON
"""
from rest_framework import serializers

from euser.models import Role, Permission, RolePermission, EUserPassword, EUserSecurityQuestion, EUser, \
	ExtendedEUserPermission


class RoleSerializer(serializers.ModelSerializer):
	"""
		Serializer for Role Model
	"""
	class Meta:
		model = Role
		fields = '__All__'


class PermissionSerializer(serializers.ModelSerializer):
	"""
		Serializer for Permission Model
	"""
	class Meta:
		model = Permission
		fields = '__All__'


class RolePermissionSerializer(serializers.ModelSerializer):
	"""
		Serializer for RolePermission Model
	"""
	class Meta:
		model = RolePermission
		fields = '__All__'


class EUserPasswordSerializer(serializers.ModelSerializer):
	"""
		Serializer for EUserPassword Model
	"""
	class Meta:
		model = EUserPassword
		fields = '__All__'


class EUserSecurityQuestionSerializer(serializers.ModelSerializer):
	"""
		Serializer for EUserSecurityQuestion Model
	"""
	# @TODO Move to customers
	class Meta:
		model = EUserSecurityQuestion
		fields = '__All__'


class EUserSerializer(serializers.ModelSerializer):
	"""
		Serializer for EUser Model
	"""
	class Meta:
		model = EUser
		fields = '__All__'


class ExtendedEUserPermissionSerializer(serializers.ModelSerializer):
	"""
		Serializer for ExtendedEUserPermission Model
	"""
	class Meta:
		model = ExtendedEUserPermission
		fields = '__All__'







