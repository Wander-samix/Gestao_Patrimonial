from rest_framework import viewsets
from core.models import LogAcao
from interface.serializers.log_acao_serializer import LogAcaoSerializer

class LogAcaoViewSet(viewsets.ModelViewSet):
    queryset = LogAcao.objects.all()
    serializer_class = LogAcaoSerializer
