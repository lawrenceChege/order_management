""" This module holds services for customer module """

from base.backend.service_base import ServiceBase
from customers.models import Customer


class CustomerService(ServiceBase):
	""" Service for customer module """
	manager = Customer.objects
