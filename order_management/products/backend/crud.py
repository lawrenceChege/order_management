"""
This module holds administration for LoanType, LoanProduct and product settings
"""

import logging
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpRequest
from base.backend.services import StateService
from base.backend.utils.validators import validate_name, validate_email,  validate_uuid4
from corporate.backend.serializers import CorporateSerializer
from corporate.backend.services import CorporateService
from audit.administration.audit_administration import TransactionLogBase
from product.backend.services import LoanTypeService, LoanProductService

lgr = logging.getLogger(__name__)


class ProductAdministration(TransactionLogBase):
    """
    This class handles the methods for creating, updating, reading and deleting
    product
    """

    def add_product(self, request, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
        """
        This method handles creating of a product
        @params request: Http request
        @type request: HttpRequest
        @params kwargs: Key value object containing the data
        @type kwargs: dict
        @return Json response
        """
        transaction = self.log_transaction(
            transaction_type="Add Product", trace="product_administration/add_product", request=request)
        try:
            if transaction is None:
                return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
            name = kwargs.pop("name")
            corporate_id = kwargs.pop("corporate")
            loan_type_id = kwargs.get("loan_type")
            ussd_enabled = kwargs.get("ussd_enabled")
            mobile_app_enabled = kwargs.get("mobile_app_enabled")
            ui_enabled = kwargs.get("ui_enabled")
            corporate_web_enabled = kwargs.get("corporate_web_enabled")
            k = {}
            if not validate_uuid4(corporate_id):
                self.mark_transaction_failed(transaction, description="Invalid corporate", code="999.004.006")
                return {
                    "code": "999.004.006", "message": "Invalid corporate", 'transaction': str(transaction.id)}
            corporate = CorporateService().get(pk=corporate_id)
            if not corporate:
                self.mark_transaction_failed(transaction, code='300.001.002', description='Corporate not found')
                return {'code': '300.001.002', 'message': 'Corporate not found', 'transaction': str(transaction.id)}
            k['corporate'] = corporate
            if name and not validate_name(str(name)):
                self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid name')
                return {
                    'code': '999.002.006',
                    'message': f'{name} is invalid. Name should have min of 3 alphabetical characters ',
                    'transaction_id': str(transaction.id)}
            k['name'] = name
            if loan_type_id:
                if not validate_uuid4(loan_type_id):
                    self.mark_transaction_failed(transaction, description="Invalid loan type", code="999.004.006")
                    return {
                        "code": "999.004.006", "message": "Invalid loan type", 'transaction': str(transaction.id)}
            loan_type = LoanTypeService().get(pk=loan_type_id)
            if not loan_type:
                self.mark_transaction_failed(transaction, description="Loan type not found", code="600.001.002")
                return {
                    "code": "600.001.002", "message": "Loan type not found", 'transaction': str(transaction.id)}
            k['loan_type'] = loan_type
            if ussd_enabled:
                k['ussd_enabled'] = ussd_enabled
            if corporate_web_enabled:
                k['corporate_web_enabled'] = corporate_web_enabled
            if ussd_enabled:
                k['mobile_app_enabled'] = mobile_app_enabled
            if ussd_enabled:
                k['ui_enabled'] = ui_enabled
            loan_product = LoanProductService().create(**k)
            if not loan_product:
                self.mark_transaction_failed(transaction, description="product was not added", code="600.002.001")
                return {"code": "600.002.001", "message": "product was not added.", "transaction": str(transaction.id)}
            self.complete_transaction(transaction, code='100.000.000', description='Success')
            return {'code': '100.000.000', 'message': 'Success', 'data': {'product': str(corporate.id)}}
        except Exception as e:
            self.mark_transaction_failed(transaction, description=str(e), code="999.999.999")
            return {
                "code": "999.999.999", "message": "Exception adding loan product",
                "error": str(e), 'transaction': str(transaction.id)}

    def update_product(self, request, **data) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
        """
        This method handles updating of a product
        @params request: Http request
        @type request: HttpRequest
        @params data: Key value object containing the data
        @type data: dict
        @return JsonResponse
        """
        transaction = self.log_transaction(
            transaction_type="Edit Product", trace='product/update_product', request=request)
        try:
            if not transaction:
                return {'code': '800.001.001', 'message': 'Failed to log transaction.'}
            product_id = data.get("product")
            loan_type_id = data.get("loan_type")
            ussd_enabled = data.get("ussd_enabled")
            mobile_app_enabled = data.get("mobile_app_enabled")
            ui_enabled = data.get("ui_enabled")
            corporate_web_enabled = data.get("corporate_web_enabled")
            name = data.get("name")
            state = data.get("state")
            if product_id and not validate_uuid4(product_id):
                self.mark_transaction_failed(transaction, code='999.005.006', description='Invalid product')
                return {'code': '999.005.006', 'message': 'Product not valid', 'transaction': str(transaction.id)}
            product = LoanProductService().get(pk=product_id)
            if not product:
                self.mark_transaction_failed(transaction, description="Product not found", code="600.002.002")
                return {
                    "code": "600.002.002", "message": "Product not found", 'transaction': str(transaction.id)}
            if name and not validate_name(str(name)):
                self.mark_transaction_failed(transaction, code='999.002.006', description='Invalid name')
                return {
                    'code': '999.002.006',
                    'message': f'{name} is invalid. Name should have min of 3 alphabetical characters ',
                    'transaction_id': str(transaction.id)}
            if loan_type_id and not validate_email(str(loan_type_id)):
                self.mark_transaction_failed(transaction, description="Invalid loan type", code="999.004.006")
                return {
                    "code": "999.004.006", "message": "Invalid loan type", 'transaction': str(transaction.id)}
            loan_type = LoanTypeService().get(pk=loan_type_id)
            if not loan_type:
                self.mark_transaction_failed(transaction, description="Loan type not found", code="600.001.002")
                return {
                    "code": "600.001.002", "message": "Loan type not found", 'transaction': str(transaction.id)}
            if state:
                state = StateService().get(pk=state)
            to_update = {
                'name': name, 'if ussd_enabled:': ussd_enabled, 'loan_type': loan_type,
                'corporate_web_enabled': corporate_web_enabled, 'mobile_app_enabled': mobile_app_enabled,
                'ui_enabled': ui_enabled, 'state': state}
            data = {k: v for k, v in to_update.items() if v is not None}
            updated_product = LoanProductService().update(pk=product_id, **data)
            if updated_product < 1:
                self.mark_transaction_failed(
                    transaction, code='600.002.007', description='Loan product failed to update')
                return {
                    'code': '600.002.007', 'message': 'Loan product failed to update', 'transaction': str(transaction.id)}
            serializer = CorporateSerializer(updated_product)
            self.complete_transaction(transaction, code='100.000.000', description='Success')
            return {
                'code': '100.000.000', 'message': 'Success', 'data': serializer.data}
        except Exception as e:
            self.mark_transaction_failed(transaction, code='999.999.999', description=str(e))
            return {
                'code': '999.999.999', 'message': 'Error when updating loan product', 'transaction': str(transaction.id)}

    def get_products(self, **kwargs) -> JsonResponse('data', encoder=DjangoJSONEncoder, safe=False):
        """
        This method handles  reading of products
        @params request: Http request
        @type request: HttpRequest
        @params kwargs: Key value object containing the data
        @type kwargs: dict
        @return JsonResponse
        @rtype JsonResponse with response code and data
        """
        try:
            corporate_id = kwargs.pop('corporate')
            if not validate_uuid4(corporate_id):
                return {"code": "999.005.006", "message": "Invalid corporate"}
            corporate = CorporateService().get(pk=corporate_id)
            if not corporate:
                return {"code": "300.001.002", "message": "Corporate not found"}
            products = LoanProductService().filter(corporate=corporate)
            if not products:
                return {"code": "600.002.002", "message": "Loan products not found"}
            return {"code": "100.000.000", "message": "Success", 'data': {"products": list(products.values())}}
        except Exception as e:
            return {"code": "999.999.999", "message": "Error fetching a products"}



