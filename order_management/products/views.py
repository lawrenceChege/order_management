import logging
from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .backend.product_base import ProductBase

lgr = logging.getLogger(__name__)


@api_view(['POST'])
def create_product(request):
	"""
		This is the API endpoint for posting a loan product
		@param request: Django HTTP request.
		request contains data = {
				name
				description
				category
				quantity
				currency
				price
				status
				}
		@type request: WSGIRequest
		@return: JsonResponse with the response code obtained from processing this request.
		@rtype: JsonResponse
	"""
	try:
		return JsonResponse(ProductBase().add_product(request))
	except Exception as e:
		lgr.error("add_product Exception: %s", e)
		return {"code": "999.999.999", "error": str(e)}


@api_view(('GET',))
def product_list(request):
	"""
		This api end point returns List all corporate  products
		The endpoint for loan application
		@param request: Django HTTP request.
		request contains data = {- corporate}
		@type request: WSGIRequest
		@return: JsonResponse with the response code obtained from processing this request.
		@rtype: JsonResponse
		"""
	try:
		return JsonResponse(ProductBase().get_all_products(request))
	except Exception as e:
		lgr.error("get_products Exception: %s", e)
		return {"code": "999.999.999", "error": str(e)}


@api_view(('GET',))
def product_detail(request):
	"""
		This api endpoint returns detail of specific loan product
	"""
	try:
		return JsonResponse(ProductBase().get_product(request))
	
	except Exception as e:
		
		lgr.error(
			{
				'code': '200.002.001',
				'error': "an error occurred ",
				'msg': e,
				'trace': "product/views/product_details"
			}
		)
		return JsonResponse(
			{
				'code': '200.100.001',
				'trace': 'product/views/loan_product_detail',
				'description': str(e)
			}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('PUT',))
def update_product(request):
	"""
		This api endpoint update a single record of product
	"""
	
	try:
		return JsonResponse(ProductBase().update_product(request))
	except Exception as e:
		lgr.error(
			{
				'code': '200.002.001',
				'error': e, 'trace': 'product/views/update_loan_product',
				'msg': "failed to updated loan product"
			}
		)
		return Response({
			'code': '200.002.002',
			'error': str(e),
			'trace': 'product/views/update_loan_product',
			'description': "failed to updated loan product"
		}, status.HTTP_400_BAD_REQUEST)


@api_view(('DELETE',))
def delete_loan_product(request):
	""" Api end point for deleting  Loan product
	deletes a single product using it's pk
	"""
	
	try:
		
		return JsonResponse(ProductBase().delete_product(request))
	except Exception as e:
		lgr.log(
			{
				'code': '200.100.002',
				'message': e,
				'trace': 'product/views/delete_loan_product',
				'description': "failed to delete loan product"
			}
		)
		return Response(
			{
				'code': '200.100.002',
				'msg': str(e),
				'trace': 'product/views/delete_loan_product',
				'description': "failed to delete loan product"
			}
		)
