from rest_framework import serializers
from core.models import LogAcao

class LogAcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAcao
        fields = '__all__'
