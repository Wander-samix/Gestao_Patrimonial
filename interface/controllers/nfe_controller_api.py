from rest_framework import viewsets
from core.models import NFe
from interface.serializers.nfe_serializer import NFeSerializer

class NFeViewSet(viewsets.ModelViewSet):
    queryset = NFe.objects.all()
    serializer_class = NFeSerializer
