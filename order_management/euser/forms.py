
"""
The forms for EUser module.
"""
from django import forms
from django.contrib.auth import (password_validation, )
from django.utils.translation import gettext_lazy as _

from base.base_forms import ReadOnlyPasswordHashField, ReadOnlySecurityCodeHashField, UsernameField
from euser.models import EUser, EUserPassword


class EUserChangeForm(forms.ModelForm):
	"""The form for updating the user."""

	password = ReadOnlyPasswordHashField(
		label = _("Password"),
		help_text = _(
			"Raw passwords are not stored, so you won't see this "
			"user's password, but you can change the password using "
			"<a href=\"../password/\">this form</a>."
		),
	)

	security_code = ReadOnlySecurityCodeHashField(
		label = _("Security Code"),
		help_text = _(
			"Raw security codes are not stored, so you won't see this "
			"user's security code. This can be changed through API calls."
		),
	)

	class Meta(object):
		"""Our meta data for the form"""
		model = EUser
		fields = '__all__'
		field_classes = {'username': UsernameField}

	def __init__(self, *args, **kwargs):
		super(EUserChangeForm, self).__init__(*args, **kwargs)


class EUserPasswordChangeForm(forms.ModelForm):
	"""The form for updating the user password."""

	password = ReadOnlyPasswordHashField(
		label = _("Password"),
		help_text = _(
			"Raw passwords are not stored, so you won't see this "
			"user's password, but you can change the password using "
			"<a href=\"../password/\">this form</a>."
		),
	)

	class Meta(object):
		"""Our meta data for the form"""
		model = EUserPassword
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(EUserPasswordChangeForm, self).__init__(*args, **kwargs)

	def clean_password(self):
		"""
		Regardless of what the user provides, return the initial value.
		This is done here, rather than on the field, because the
		field does not have access to the initial value
		"""
		return self.initial["password"]


class AdminPasswordChangeForm(forms.Form):
	"""A form used to change the password of a user in the admin interface."""

	error_messages = {
		'password_mismatch': _("The two password fields didn't match."),
	}
	required_css_class = 'required'
	password1 = forms.CharField(
		label = _("Password"),
		widget = forms.PasswordInput(attrs = {'autofocus': True}),
		strip = False,
		help_text = password_validation.password_validators_help_text_html(),
	)
	password2 = forms.CharField(
		label = _("Password (again)"),
		widget = forms.PasswordInput,
		strip = False,
		help_text = _("Enter the same password as before, for verification."),
	)

	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)

	def clean_password2(self):
		"""Clean the password"""
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2:
			if password1 != password2:
				raise forms.ValidationError(
					self.error_messages['password_mismatch'],
					code = 'password_mismatch',
				)
		password_validation.validate_password(password2, self.user)
		return password2

	def save(self, commit = True):
		"""
		Saves the new password.
		"""
		password = self.cleaned_data["password1"]
		self.user.set_password(password)
		if commit:
			self.user.save()
		return self.user

	@property
	def changed_data(self):
		"""The data that has changed."""
		data = super(AdminPasswordChangeForm, self).changed_data
		for name in self.fields.keys():
			if name not in data:
				return []
		return ['password']
