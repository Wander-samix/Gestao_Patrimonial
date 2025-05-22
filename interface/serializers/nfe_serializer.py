from rest_framework import serializers
from core.models import NFe

class NFeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFe
        fields = '__all__'
