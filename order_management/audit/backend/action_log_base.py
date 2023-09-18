""" Creating and updating action logs"""
import logging

from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import JsonResponse, HttpRequest
from rest_framework import status


from audit.backend.action_type_base import ActionTypeBase
from audit.backend.generate_code import generate_internal_reference
from audit.backend.services import ActionTypeService, ActionService
from base.backend.get_request_data import get_request_data
from base.backend.services import StateService


lgr = logging.getLogger(__name__)


class ActionLogBase(ActionTypeBase):
    """The class for logging actions."""

    @staticmethod
    def log_action(action_type: str, trace: str, request: HttpRequest, **kwargs):
        """
        Logs an action of the given type having the provided arguments.
        If action reference is not passed, it's generated. Same case for state, defaults to Active.
        @param request: The http request
        @type request: HttpRequest
        @param action_type: The name of the type of action we are creating.
        @type action_type: str
        @param trace: The position of the function/method.
        @type trace: str
        @param kwargs: Key word arguments to generate the transaction with.
        @return: The created transaction.
        @rtype: Transaction | None
        """
        try:
            if action_type:
                action_type = ActionTypeService().get(name=action_type)
                if not action_type:
                    lgr.error("Action Type not Found")
                    return None
            if not trace:
                lgr.error("Trace not provided")
                return None
            user_id = getattr(request, 'user', kwargs.get('user', None))
            if user_id:
                user = User.objects.get(pk=user_id)
                kwargs['user'] = user
                if not user:
                    lgr.error("User Not Found")
            with transaction.atomic():
                state = StateService().get(name='Active')
                last_ref = ActionService(True).filter().order_by('-date_created').first()
                reference = generate_internal_reference(None if last_ref is None else last_ref.reference)
                kwargs['reference'] = reference
                if not reference:
                    lgr.error("Unable to generate next reference")
                if request:
                    data = get_request_data(request)
                    if data:
                        kwargs['source_ip'] = data.get('source_ip', None)
                return ActionService().create(request=request, action_type=action_type, state=state, **kwargs)
        except Exception as e:
            lgr.exception('log_action Exception: %s', e)
        return None

    def complete_action(self, action_obj, code: str,  description: str, **kwargs):
        """
        Marks the action object as complete.
        @param action_obj: The action we are updating.
        @type action_obj: action
        @param code: The success code for the action.
        @type code: str
        @param description: The message of success.
        @type description: str
        @param kwargs: Any key->word arguments to pass to the method.
        @return: The action updated.
        @rtype: action | None
        """
        try:
            if not code:
                lgr.exception("Code not provided")
                return None
            if not description:
                lgr.exception("Description not provided")
                return None

            if not action_obj:
                lgr.exception("Action not provided")
                return None
            if kwargs is None:
                kwargs = {'state': StateService().get(name='Complete')}
            elif 'state' not in kwargs:
                kwargs['state'] = StateService().get(name='Complete')
            return ActionService().update(action_obj.id, code=code, description=description, **kwargs)
        except Exception as e:
            lgr.exception('complete_action Exception: %s', e)
        return None

    def mark_action_failed(self, action_obj, code: str, description: str, **kwargs):
        """
        Marks the action object as Failed.
        @param action_obj: The action we are updating.
        @type action_obj: action
        @param code: The success code for the action.
        @type code: str
        @param description: The message of success.
        @type description: str
        @param kwargs: Any key->word arguments to pass to the method.
        @return: The action updated.
        @rtype: action | None
        """
        try:
            if not code:
                lgr.exception("Code not provided")
                return None
            if not description:
                lgr.exception("Description not provided")
                return None
            if not action_obj:
                lgr.exception("action not provided")
                return None
            if kwargs is None:
                kwargs = {'state': StateService().get(name='Failed')}
            else:
                kwargs['state'] = StateService().get(name='Failed')
            return ActionService().update(action_obj.id, code=code, description=description, **kwargs)
        except Exception as e:
            lgr.exception('mark_action_failed Exception: %s', e)
        return None

    def get_all_actions(self, request, **kwargs: dict) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
        """
        This method helps retrieve all actions in the system.
        This is useful for an audit on our system.
        """
        action_log = self.log_action(action_type="Get all actions", request=request, **kwargs)
        try:

            if not action_log:
                return JsonResponse({
                    'code': '800.003.404',
                    'message': 'Failed to create action'
                }, status=status.HTTP_404_NOT_FOUND)
            actions = ActionService().filter()
            print(actions)
            if actions.count() < 1:
                self.mark_action_failed(
                    action_log, code='800.002.404', description='No actions found',
                    trace="audit.backend.ActionLogBase.get_all_transactions", **kwargs)
                return JsonResponse({
                    'code': '800.002.404',
                    'message': 'No actions found',
                    'action_id': f'{action_log.id}'
                }, status=status.HTTP_404_NOT_FOUND)
            action_data = []
            for log in actions:
                data = {
                    "id": log.id,
                    "date_modified": log.date_modified,
                    "date_created": log.date_created,
                    "reference": log.reference,
                    "source_ip": log.source_ip or None,
                    "request": log.request,
                    "code": log.status_code,
                    "trace": log.trace,
                    "description": log.description,
                    "user": None if log.user is None else log.user.username,
                    "action_type": log.action_type.name,
                    "state": log.state.name
                }
                action_data.append(data)

            try:
                self.complete_action(
                    action_log, code='200.000.000', description='Successfully retrieved all actions',
                    trace="audit.backend.ActionLogBase.get_all_actions", **kwargs)
                return JsonResponse({
                    'code': '200.000.000',
                    'message': 'All actions found',
                    'data': action_data
                }, status=status.HTTP_200_OK)

            except Exception as e:
                self.mark_action_failed(action_log, code='800.888.500', description=str(e),
                    trace="audit.backend.ActionLogBase.get_all_transactions", **kwargs)
                return JsonResponse({
                    'code': '800.888.500',
                    'message': 'Failed to serialize',
                    'error': str(e),
                    'transaction_id': f'{action_log.id}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            self.mark_action_failed(action_log, code='800.888.500', description=str(e),
                trace="audit.backend.ActionLogBase.get_all_transactions", **kwargs)
            return JsonResponse({
                'code': '800.888.500',
                'message': 'Failed to get all actions',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

