""" Audit module services"""

from audit.models import Action, ActionType
from base.backend.service_base import ServiceBase


class ActionService(ServiceBase):
    """
        The service for handling CRUD events for action model
    """
    manager = Action.objects


class ActionTypeService(ServiceBase):
    """
        The service for handling CRUD events for action type model
    """
    manager = ActionType.objects
