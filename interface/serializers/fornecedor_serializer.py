from rest_framework import serializers
from core.models import Fornecedor

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'
