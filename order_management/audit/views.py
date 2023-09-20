from rest_framework import viewsets
from rest_framework import permissions
from .backend.serializer import ActionSerializer

from .models import Action


class ActionViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows actions to be viewed or edited.
	"""
	queryset = Action.objects.all().order_by('-date_created')
	serializer_class = ActionSerializer
	permission_classes = [permissions.IsAuthenticated]
