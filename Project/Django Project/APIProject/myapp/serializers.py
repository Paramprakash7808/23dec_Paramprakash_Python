from rest_framework import serializers
from .models import *

class StudSerial(serializers.Serializer):
    class Meta:
        model = Studinfo
        fields = '__all__'