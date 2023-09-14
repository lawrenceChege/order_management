import uuid

from django.contrib.admin.utils import unquote
from django.utils.encoding import force_text
from django.utils.html import escape
from django.conf import settings
from django.urls import re_path
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR, csrf_protect_m
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.admin import sensitive_post_parameters_m
from django.core.exceptions import PermissionDenied
from django.db import transaction, router
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _

from api.models import Identity
from euser.forms import EUserPasswordChangeForm, EUserChangeForm, AdminPasswordChangeForm
from euser.models import EUserPassword, EUserSecurityQuestion, ExtendedEUserPermission, EUser, Role, Permission, \
	RolePermission


class EUserPasswordInlineAdmin(admin.StackedInline):
	"""
	This class registers EUserPassword model with backend Admin.
	This is a stacked inline admin form, so, do we register here? Of course not :-*
	"""
	model = EUserPassword

	extra = 1

	form = EUserPasswordChangeForm

	def get_queryset(self, request):
		"""Limit the queryset for passwords to the last 3"""
		qs = super(EUserPasswordInlineAdmin, self).get_queryset(request)
		filtered = qs[:3].values_list('id', flat=True)
		return qs.filter(id__in=filtered)

	def has_add_permission(self, request, obj=None):
		"""Disable direct adding."""
		request_id = uuid.uuid4()
		url_data = request.path.strip('/').split('/')[:2:-1]
		if len(url_data) == 2:
			# noinspection PyBroadException
			try:
				request_id = str(url_data[1])
			except Exception:
				pass
		if EUserPassword.objects.filter(euser__id=request_id).exists():
			return False
		return True

	def has_delete_permission(self, request, obj=None):
		"""Disable direct deletion"""
		return False


class EUserSecurityQuestionInlineAdmin(admin.TabularInline):
	"""
	This class registers EUserSecurityQuestion model with backend Admin.
	This is a stacked inline admin form, so, do we register here? Of course not :-*
	"""
	model = EUserSecurityQuestion

	extra = 1

	def get_queryset(self, request):
		"""Limit the queryset for passwords to the last 3"""
		qs = super(EUserSecurityQuestionInlineAdmin, self).get_queryset(request)
		filtered = qs[:3].values_list('id', flat=True)
		return qs.filter(id__in=filtered)

	def has_add_permission(self, request, obj=None):
		"""Disable direct adding."""
		return False  # Disable adding security questions from Admin

	def has_delete_permission(self, request, obj=None):
		"""Disable direct deletion"""
		return False


class ExtendedEUserPermissionInline(admin.TabularInline):
	"""
	This class registers the ExtendedUserPermission model with the admin backend
	"""
	model = ExtendedEUserPermission

	extra = 1

	def has_delete_permission(self, request, obj=None):
		"""Disable direct deletion"""
		return False


@admin.register(EUser)
class EUserAdmin(admin.ModelAdmin):
	"""
	This class registers User admin model and displays User details on the admin backend
	"""
	list_display = (
		'username', 'branch', 'phone_number', 'email', 'role', 'state', 'last_activity', 'date_modified',
		'date_created')
	search_fields = (
		'branch__name', 'branch__corporate__name', 'username', 'phone_number', 'email', 'role__name', 'state__name')
	inlines = [EUserSecurityQuestionInlineAdmin, ExtendedEUserPermissionInline, EUserPasswordInlineAdmin]
	list_filter = ('date_created', 'is_active', 'is_staff', 'is_superuser')

	fieldsets = (
		(
			'Personal Details', {
				'fields': (('username', 'email'), 'phone_number', ('branch', 'role'))
			}),
		('Other Info', {'fields': ('first_name', 'last_name', 'other_name', 'security_code')}),
		('Status', {'fields': ('state', ('is_active', 'is_staff', 'is_superuser'))}),
		('Important Dates', {'fields': ('last_login',)})
	)

	form = EUserChangeForm
	change_password_form = AdminPasswordChangeForm
	change_user_password_template = None

	def get_urls(self):
		"""Appends our custom password change form to our request"""
		return [re_path(
			r'^(.+)/password/$',
			self.admin_site.admin_view(self.user_change_password),
			name = 'auth_user_password_change',
		), ] + super(EUserAdmin, self).get_urls()

	@sensitive_post_parameters_m
	@csrf_protect_m
	def add_view(self, request, form_url='', extra_context=None):
		"""Adds the respective view depending on the current model state."""
		with transaction.atomic(using=router.db_for_write(self.model)):
			return self._add_view(request, form_url, extra_context)

	# noinspection PyProtectedMember
	def _add_view(self, request, form_url='', extra_context=None):
		"""It's an error for a user to have add permission but NOT change
		permission for users. If we allowed such users to add users, they
		could create superusers, which would mean they would essentially have
		the permission to change users. To avoid the problem entirely, we
		disallow users from adding users if they don't have change
		permission."""
		if not self.has_change_permission(request):
			if self.has_add_permission(request) and settings.DEBUG:
				# Raise Http404 in debug mode so that the user gets a helpful
				# error message.
				raise Http404(
					'Your user does not have the "Change user" permission. In '
					'order to add users, Django requires that your user '
					'account have both the "Add user" and "Change user" '
					'permissions set.')
			raise PermissionDenied
		if extra_context is None:
			extra_context = {}
		username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
		defaults = {
			'auto_populated_fields': (),
			'username_help_text': username_field.help_text,
		}
		extra_context.update(defaults)
		return super(EUserAdmin, self).add_view(request, form_url, extra_context)

	# noinspection PyProtectedMember
	@sensitive_post_parameters_m
	def user_change_password(self, request, user_id, form_url=''):
		"""Allows changing the password using a different form."""
		if not self.has_change_permission(request):
			raise PermissionDenied
		user = self.get_object(request, unquote(user_id))
		if user is None:
			raise Http404(_('%(name)s object with primary key %(id)r does not exist.') % {
				'name': force_text(self.model._meta.verbose_name),
				'key': escape(user_id),
			})
		if request.method == 'POST':
			form = self.change_password_form(user, request.POST)
			if form.is_valid():
				form.save()
				change_message = self.construct_change_message(request, form, None)
				self.log_change(request, user, change_message)
				msg = ugettext('Password changed successfully.')
				messages.success(request, msg)
				update_session_auth_hash(request, form.user)
				return HttpResponseRedirect(
					reverse(
						'%s:%s_%s_change' % (
							self.admin_site.name,
							user._meta.app_label,
							user._meta.model_name,
						),
						args=(user.pk,),
					)
				)
		else:
			form = self.change_password_form(user)

		fieldsets = [(None, {'fields': list(form.base_fields)})]
		admin_form = admin.helpers.AdminForm(form, fieldsets, {})

		context = {
			'title': _('Change password: %s') % escape(user.get_username()),
			'adminForm': admin_form,
			'form_url': form_url,
			'form': form,
			'is_popup': (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
			'add': True,
			'change': False,
			'has_delete_permission': False,
			'has_change_permission': True,
			'has_absolute_url': False,
			'opts': self.model._meta,
			'original': user,
			'save_as': False,
			'show_save': True,
		}
		context.update(self.admin_site.each_context(request))

		request.current_app = self.admin_site.name

		return TemplateResponse(
			request,
			self.change_user_password_template or
			'admin/auth/user/change_password.html',
			context,
		)

	def response_add(self, request, obj, post_url_continue = None):
		"""
		Determines the HttpResponse for the add_view stage. It mostly defers to
		its superclass implementation but is customized because the User model
		has a slightly different workflow.
		"""
		# We should allow further modification of the user just added i.e. the
		# 'Save' button should behave like the 'Save and continue editing'
		# button except in two scenarios:
		# * The user has pressed the 'Save and add another' button
		# * We are adding a user in a popup
		if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
			request.POST = request.POST.copy()
			request.POST['_continue'] = 1
		return super(EUserAdmin, self).response_add(request, obj, post_url_continue)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	"""
	This class registers the Role model with the admin backend
	"""
	list_filter = ('date_created',)
	ordering = ('-date_created',)
	list_display = (
		'name', 'is_corporate_role', 'is_service_provider_role', 'is_super_admin_role', 'state', 'date_modified',
		'date_created')
	search_fields = ('name', 'description', 'state__name')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
	"""
	This class registers the Permission model with the admin backed
	"""
	list_filter = ('date_created',)
	ordering = ('-date_created',)
	list_display = (
		'name', 'simple_name', 'extendable_by_corporate', 'extendable_by_service_provider', 'parent',
		'state', 'date_modified', 'date_created')
	search_fields = ('name', 'description', 'simple_name', 'parent__simple_name', 'state__name')


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
	"""
	This class registers the RolePermission model with the admin backend
	"""
	list_filter = ('date_created',)
	ordering = ('-date_created',)
	list_display = ('role', 'permission', 'state', 'date_modified', 'date_created')
	search_fields = ('role__name', 'permission__name', 'state__name')

@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
	"""
	This class registers the RolePermission model with the admin backend
	"""
	list_filter = ('date_created',)
	ordering = ('-date_created',)
	list_display = ('euser', 'expires_at', 'state', 'date_modified', 'totp_key', 'date_created')
	search_fields = ('euser__name', 'corporate_customer__name', 'totp_key', 'state__name')

