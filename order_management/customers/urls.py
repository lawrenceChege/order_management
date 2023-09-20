from django.urls import include, path
from rest_framework import routers

from customers import views

router = routers.DefaultRouter()
router.register(r'', views.CustomerViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('register', views.register, name="register customer"),
    
]
