import re
from rest_framework import serializers
from .models import requestion_information

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = requestion_information
        fields = ['id', 'name', 'time','ip']

