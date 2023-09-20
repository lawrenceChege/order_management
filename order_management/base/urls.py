from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'states', views.StateViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'currencies', views.CurrencyViewSet)

urlpatterns = [
	path('', include(router.urls)),
	]
