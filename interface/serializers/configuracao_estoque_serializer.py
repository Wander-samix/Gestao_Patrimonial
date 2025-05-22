from rest_framework import serializers
from core.models import ConfiguracaoEstoque

class ConfiguracaoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoEstoque
        fields = '__all__'
