from rest_framework import serializers

from audit.models import Action


class ActionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Action
		fields = '__all__'
		