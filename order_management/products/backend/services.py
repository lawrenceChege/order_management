from base.backend.service_base import ServiceBase
from products.models import Product


class ProductService(ServiceBase):
	""" Service for product model """
	manager = Product.onjects
	