from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
	path('products/', views.product_list, name="product_list"),
	path('product/details/<str:pk>',views.loan_product_detail,name="product_detail"),
	path('product/create', views.create_loan_product, name="create_product"),
	path('product/update/<str:pk>',views.update_loan_product,name="update_product"),
	path('product/delete/<str:pk>',views.delete_loan_product,name="delete_product"),
]

urlpatterns = format_suffix_patterns(urlpatterns)