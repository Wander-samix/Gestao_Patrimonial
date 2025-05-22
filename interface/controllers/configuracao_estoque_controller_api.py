from rest_framework import viewsets
from core.models import ConfiguracaoEstoque
from interface.serializers.configuracao_estoque_serializer import ConfiguracaoEstoqueSerializer

class ConfiguracaoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracaoEstoque.objects.all()
    serializer_class = ConfiguracaoEstoqueSerializer
