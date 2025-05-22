from rest_framework import viewsets
from core.models import Produto
from interface.serializers.produto_serializer import ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
