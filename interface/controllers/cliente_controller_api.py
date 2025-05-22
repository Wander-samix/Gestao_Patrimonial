from rest_framework import viewsets
from core.models import Cliente
from interface.serializers.cliente_serializer import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
