from rest_framework import viewsets
from core.models import MovimentacaoEstoque
from interface.serializers.movimentacao_estoque_serializer import MovimentacaoEstoqueSerializer

class MovimentacaoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentacaoEstoque.objects.all()
    serializer_class = MovimentacaoEstoqueSerializer
