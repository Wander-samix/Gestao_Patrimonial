from rest_framework import viewsets
from core.models import Area
from interface.serializers.area_serializer import AreaSerializer

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
