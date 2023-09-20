# customer_order/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomerListCreateView, CustomerDetailView, OrderListCreateView, OrderDetailView, CustomerViewSet, \
    OrderViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
