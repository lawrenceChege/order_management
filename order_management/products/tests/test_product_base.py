from unittest import TestCase

from django.db.transaction import atomic
from mixer.backend.django import mixer

from django.db import transaction

from api.tests.test_setup import TestSetUp
from product.administration.product_administration import ProductAdministration


class TestProductBase(TestSetUp, TestCase):
    """
        Test for Product Administration
    """

    def test_add_product(self):
        corporate = mixer.blend('corporate.Corporate')
        loan_type = mixer.blend('product.LoanType', name="SAWA")
        state = mixer.blend('base.State')
        with transaction.atomic():
            data = {
                "name": "1Month", "corporate": corporate.id, "loan_type": loan_type.id,
                "ussd_enabled": True, "mobile_app_enabled": True, "ui_enabled": True,
                "corporate_web_enabled": False, "state": state}
            product = ProductAdministration().add_product(request=None, **data)
            assert product.get('code') == '800.001.001', 'should fail transaction not logged'
        mixer.blend('base.TransactionType', name='Add Product')
        with transaction.atomic():
            data = {
                "name": "2Month ", "corporate": corporate.id, "loan_type": loan_type.id,
                "ussd_enabled": True, "mobile_app_enabled": True, "ui_enabled": True,
                "corporate_web_enabled": False, "state": state}
            product = ProductAdministration().add_product(request=None, **data)
            assert product.get('code') == "100.000.000", 'should return a success code 100.000.000'
        with transaction.atomic():
            data = {
                "name": "3Month ", "corporate": "43d5d476-2a6f-4f35-aec6-d3c03bda0211214", "loan_type": loan_type.id,
                "ussd_enabled": True, "mobile_app_enabled": True, "ui_enabled": True,
                "corporate_web_enabled": False, "state": state}
            product = ProductAdministration().add_product(request="", **data)
            assert product.get('code') == '999.004.006', 'should return Error code 999.004.006 for invalid corporate'
        with transaction.atomic():
            data = {
                "name": "4Month ", "corporate": loan_type.id, "loan_type": loan_type.id,
                "ussd_enabled": True, "mobile_app_enabled": True, "ui_enabled": True,
                "corporate_web_enabled": False, "state": state}
            product = ProductAdministration().add_product(request="", **data)
            assert product.get('code') == '300.001.002', 'should return Error code 300.001.002 for corporate not found'
        with transaction.atomic():
            data = {
                "name": "7Month", "corporate": corporate.id, "loan_type": "43d5d476-2a6f-4f35-aec6-d3c03bda0211214",
                "ussd_enabled": True, "mobile_app_enabled": True, "ui_enabled": True,
                "corporate_web_enabled": False, "state": state}
            product = ProductAdministration().add_product(request=None, **data)
            assert product.get('code') == '999.004.006', 'should fail loan type invalid'
        with transaction.atomic():
            data = {
                "name": "5Month ", "corporate": corporate.id, "loan_type": corporate.id,
                "ussd_enabled": True, "mobile_app_enabled": True, "ui_enabled": True,
                "corporate_web_enabled": False, "state": state}
            product = ProductAdministration().add_product(request=None, **data)
            assert product.get('code') == '600.001.002', 'should fail loan type not found'
        with transaction.atomic():
            data = {
                "name": "4", "corporate": corporate.id, "loan_type": loan_type.id,
                "ussd_enabled": True, "mobile_app_enabled": True, "ui_enabled": True,
                "corporate_web_enabled": False, "state": state}
            product = ProductAdministration().add_product(request=None, **data)
            assert product.get('code') == '999.002.006', 'should fail,invalid name'




