"""
Create update action types
"""
import logging
from typing import Optional

from django.db.models import QuerySet

from audit.backend.services import ActionTypeService
from base.backend.services import StateService

lgr = logging.getLogger(__name__)


class ActionTypeBase(object):
    """
    Administration for action type
    """
    @staticmethod
    def create_if_not_exits(name: str) -> Optional[QuerySet]:
        try:
            state = StateService().get(name="Active")
            action_type = ActionTypeService().get(name=name)
            if action_type:
                return None
            return ActionTypeService.create(name=name, state=state)
        except Exception as e:
            lgr.exception(str(e))
            return None

