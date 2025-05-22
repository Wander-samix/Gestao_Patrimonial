from rest_framework import viewsets
from core.models import ItemPedido
from interface.serializers.item_pedido_serializer import ItemPedidoSerializer

class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer
