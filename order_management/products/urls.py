from django.urls import path, include
from rest_framework import routers
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
urlpatterns = [
	path('', include(router.urls)),
	path('', views.product_list, name="product_list"),
	path('details/<str:pk>', views.product_detail, name="product_detail"),
	path('create', views.create_product, name="create_product"),
	path('update/<str:pk>', views.update_product, name="update_product"),
	path('delete/<str:pk>', views.delete_product, name="delete_product"),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
