from rest_framework import viewsets
from core.models import Fornecedor
from interface.serializers.fornecedor_serializer import FornecedorSerializer

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
