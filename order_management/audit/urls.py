from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'actions', views.ActionViewSet)

urlpatterns = [
	path('', include(router.urls)),
	]
