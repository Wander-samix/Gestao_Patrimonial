from rest_framework import viewsets
from core.models import Pedido
from interface.serializers.pedido_serializer import PedidoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
