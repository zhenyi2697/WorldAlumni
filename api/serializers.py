from django.forms import widgets
from rest_framework import serializers

from backend.models import *

class BindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Binding
        fields = ('id', 'bind_from', 'create_time', 'modify_time')
