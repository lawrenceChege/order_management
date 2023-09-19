	"""
	This module has helper methods for product views
	"""
	from products.backend.seriallizers import ProductSerializer
	from products.backend.services import ProductService
	import logging
	from django.core.serializers.json import DjangoJSONEncoder
	from django.http import JsonResponse, HttpRequest
	
	from audit.backend.action_log_base import ActionLogBase
	from base.backend.get_request_data import get_request_data
	from base.backend.services import StateService, CategoryService, CurrencyService
	from base.backend.validators import validate_uuid7, validate_name, validate_amount
	
	lgr = logging.getLogger(__name__)
	
	
	class ProductBase(ActionLogBase):
		"""
		This class handles the methods for creating, updating, reading and deleting
		product
		"""
		
		def add_product(self, request) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
			"""
			This method handles creating of a product
			@params request: Http request
			@type request: HttpRequest
			@return Json response
			"""
			action = self.log_action(
				action_type="Add Product", trace="product_base/add_product", request=request)
			try:
				if action is None:
					return {'code': '800.001.001', 'message': 'Failed to log action.'}
				kwargs = get_request_data(request)
				name = kwargs.pop("name")
				category_id = kwargs.pop("category")
				price = kwargs.pop("price")
				quantity = kwargs.pop("quantity")
				currency_id = kwargs.pop("currency")
				description = kwargs.get("description")
				k = {}
				if not validate_uuid7(category_id):
					self.mark_action_failed(action, description="Invalid category", code="999.004.006")
					return {
						"code": "999.004.006", "message": "Invalid category", 'action_id': str(action.id)}
				category = CategoryService().get(pk=category_id)
				if not category:
					self.mark_action_failed(action, code='300.001.002', description='Category not found')
					return {'code': '300.001.002', 'message': 'Category not found', 'action_id': str(action.id)}
				k['category'] = category
				if not validate_uuid7(currency_id):
					self.mark_action_failed(action, description="Invalid currency", code="999.004.006")
					return {
						"code": "999.004.006", "message": "Invalid currency", 'action_id': str(action.id)}
				currency = CurrencyService().get(pk=currency_id)
				if not currency:
					self.mark_action_failed(action, code='300.001.002', description='Currency not found')
					return {'code': '300.001.002', 'message': 'Currency not found', 'action_id': str(action.id)}
				k['currency'] = currency
				if name and not validate_name(str(name)):
					self.mark_action_failed(action, code='999.002.006', description='Invalid name')
					return {
						'code': '999.002.006',
						'message': f'{name} is invalid. Name should have min of 3 alphabetical characters ',
						'action_id': str(action.id)}
				k['name'] = name
				if not validate_amount(price):
					self.mark_action_failed(action, code='300.001.002', description='price not valid amount')
					return {"code": "300.001.002", "message": "Price is not a valid amount", "action_id": str(action.id)}
				k['price'] = price
				if not isinstance(int(quantity), int):
					self.mark_action_failed(action, code='300.001.002', description='Quantity not valid')
					return {"code": "300.001.002", "message": "Quantity is not a valid number",
							"action_id": str(action.id)}
				k['quantity'] = quantity
				k['description'] = description
				product = ProductService().create(**k)
				if not product:
					self.mark_action_failed(action, description="product was not added", code="600.002.001")
					return {"code": "600.002.001", "message": "product was not added.", "action_id": str(action.id)}
				self.complete_action(action, code='100.000.000', description='Success')
				return {'code': '100.000.000', 'message': 'Success', 'data': {'product': str(product.id)}}
			except Exception as e:
				self.mark_action_failed(action, description=str(e), code="999.999.999")
				return {
					"code": "999.999.999", "message": "Exception adding product",
					"error": str(e), 'action': str(action.id)}
		
		def update_product(self, request) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
			"""
			This method handles updating of a product
			@params request: Http request
			@type request: HttpRequest
			@params data: Key value object containing the data
			@type data: dict
			@return JsonResponse
			"""
			action = self.log_action(
				action_type="Edit Product", trace='backend/product_base/update_product', request=request)
			try:
				if not action:
					return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
				kwargs = get_request_data(request)
				product_id = kwargs.get("product")
				name = kwargs.pop("name")
				category_id = kwargs.pop("category")
				price = kwargs.pop("price")
				quantity = kwargs.pop("quantity")
				currency_id = kwargs.pop("currency")
				description = kwargs.get("description")
				state = kwargs.get("state")
				if product_id and not validate_uuid7(product_id):
					self.mark_action_failed(action, code='999.005.006', description='Invalid product')
					return {'code': '999.005.006', 'message': 'Product not valid', 'action': str(action.id)}
				product = ProductService().get(pk=product_id)
				if not product:
					self.mark_action_failed(action, description="Product not found", code="600.002.002")
					return {
						"code": "600.002.002", "message": "Product not found", 'action': str(action.id)}
				if not validate_uuid7(category_id):
					self.mark_action_failed(action, description="Invalid category", code="999.004.006")
					return {
						"code": "999.004.006", "message": "Invalid category", 'action_id': str(action.id)}
				category = CategoryService().get(pk=category_id)
				if not category:
					self.mark_action_failed(action, code='300.001.002', description='Category not found')
					return {'code': '300.001.002', 'message': 'Category not found', 'action_id': str(action.id)}
				if not validate_uuid7(currency_id):
					self.mark_action_failed(action, description="Invalid currency", code="999.004.006")
					return {
						"code": "999.004.006", "message": "Invalid currency", 'action_id': str(action.id)}
				currency = CurrencyService().get(pk=currency_id)
				if not currency:
					self.mark_action_failed(action, code='300.001.002', description='Currency not found')
					return {'code': '300.001.002', 'message': 'Currency not found', 'action_id': str(action.id)}
				if name and not validate_name(str(name)):
					self.mark_action_failed(action, code='999.002.006', description='Invalid name')
					return {
						'code': '999.002.006',
						'message': f'{name} is invalid. Name should have min of 3 alphabetical characters ',
						'action_id': str(action.id)}
				
				if state:
					state = StateService().get(pk=state)
				to_update = {
					'name': name, 'category:': category, 'currency': currency,
					'description': description, 'price': price,
					'quantity': quantity, 'state': state}
				data = {k: v for k, v in to_update.items() if v is not None}
				updated_product = ProductService().update(pk=product_id, **data)
				if updated_product < 1:
					self.mark_action_failed(
						action, code='600.002.007', description='Product failed to update')
					return {
						'code': '600.002.007', 'message': 'Product failed to update',
						'action': str(action.id)}
				serializer = ProductSerializer(updated_product)
				self.complete_action(action, code='100.000.000', description='Success')
				return {
					'code': '100.000.000', 'message': 'Success', 'data': serializer.data}
			except Exception as e:
				self.mark_action_failed(action, code='999.999.999', description=str(e))
				return {
					'code': '999.999.999', 'message': 'Error when updating loan product',
					'action': str(action.id)}
		
		def get_all_product(self, request) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
			"""
			This method handles  reading of products
			@params request: Http request
			@type request: HttpRequest
			@return JsonResponse
			@rtype JsonResponse with response code and data
			"""
			
			try:
				kwargs = get_request_data(request)
				products = ProductService().filter()
				if not products:
					return {
						'code': '600.002.404', 'message': 'Products not found'}
				serializer = ProductSerializer(products)
				return {
					'code': '100.000.000', 'message': 'Success', 'data': serializer.data}
			except Exception as e:
				return {"code": "999.999.999", "message": "Error fetching products"}
	
		
		def get_product(self, request) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
			"""
			This method handles  reading of products
			@params request: Http request
			@type request: HttpRequest
			@return JsonResponse
			@rtype JsonResponse with response code and data
			"""
			action = self.log_action(
				action_type="Get Product", trace='backend/product_base/_product', request=request)
			try:
				kwargs = get_request_data(request)
				product_id = kwargs.pop("product")
				if product_id and not validate_uuid7(product_id):
					self.mark_action_failed(action, code='999.005.006', description='Invalid product')
					return {'code': '999.005.006', 'message': 'Product not valid', 'action': str(action.id)}
				product = ProductService().get(pk=product_id)
				if not product:
					self.mark_action_failed(action, description="Product not found", code="600.002.002")
					return {
						"code": "600.002.002", "message": "Product not found", 'action': str(action.id)}
				serializer = ProductSerializer(product)
				self.mark_action_complete(action, description="Product  found", code="100.000.000")
				return {
					'code': '100.000.000', 'message': 'Success', 'data': serializer.data}
			except Exception as e:
				self.mark_action_failed(action, code='999.999.999', description=str(e))
				return {
					'code': '999.999.999', 'message': 'Error when fetching loan product',
					'action': str(action.id)}
			
		def delete_product(self, request):
			""" Mark product as deleted """
		
			action = self.log_action(
				action_type="Delete Product", trace='backend/product_base/delete_product', request=request)
			try:
				kwargs = get_request_data(request)
				product_id = kwargs.pop("product")
				if product_id and not validate_uuid7(product_id):
					self.mark_action_failed(action, code='999.005.006', description='Invalid product')
					return {'code': '999.005.006', 'message': 'Product not valid', 'action': str(action.id)}
				product = ProductService().get(pk=product_id)
				if not product:
					self.mark_action_failed(action, description="Product not found", code="600.002.002")
					return {
						"code": "600.002.002", "message": "Product not found", 'action': str(action.id)}
				deleted_state = StateService.get(name="deleted")
				ProductService().update(pk=product_id, status=deleted_state)
				self.mark_action_complete(action, description="Product  deleted", code="100.000.000")
				return {
					'code': '100.000.000', 'message': 'Success'}
			except Exception as e:
				self.mark_action_failed(action, code='999.999.999', description=str(e))
				return {
					'code': '999.999.999', 'message': 'Error when deleting loan product',
					'action': str(action.id)}
				
