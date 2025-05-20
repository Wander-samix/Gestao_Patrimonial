from typing import List, Optional
from core.domain.entities.log_acao import Log_acao
from core.domain.repositories.log_acao_repository import ILog_acaoRepository
from core.models import LogAcao as LogAcaoModel

class DjangoLog_acaoRepository(ILog_acaoRepository):
    def save(self, obj: Log_acao) -> Log_acao:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Retorna a entidade de domínio com o id gerado/atualizado.
        """
        if getattr(obj, 'id', None):
            model = LogAcaoModel.objects.get(pk=obj.id)
            model.usuario_id = obj.usuario_id
            model.acao       = obj.acao
            model.detalhes   = obj.detalhes
            model.data_hora  = obj.data_hora
            model.ip         = obj.ip
            model.save(update_fields=['usuario', 'acao', 'detalhes', 'data_hora', 'ip'])
        else:
            model = LogAcaoModel.objects.create(
                usuario_id=obj.usuario_id,
                acao=obj.acao,
                detalhes=obj.detalhes,
                data_hora=obj.data_hora,
                ip=obj.ip
            )
        return Log_acao(
            id=model.id,
            usuario_id=model.usuario_id,
            acao=model.acao,
            detalhes=model.detalhes,
            data_hora=model.data_hora,
            ip=model.ip
        )

    def find_by_id(self, id: int) -> Optional[Log_acao]:
        """
        Busca Log_acao por PK; retorna None se não existir.
        """
        try:
            m = LogAcaoModel.objects.get(pk=id)
            return Log_acao(
                id=m.id,
                usuario_id=m.usuario_id,
                acao=m.acao,
                detalhes=m.detalhes,
                data_hora=m.data_hora,
                ip=m.ip
            )
        except LogAcaoModel.DoesNotExist:
            return None

    def list_all(self) -> List[Log_acao]:
        """
        Retorna todos os logs de ação como entidades de domínio.
        """
        return [
            Log_acao(
                id=m.id,
                usuario_id=m.usuario_id,
                acao=m.acao,
                detalhes=m.detalhes,
                data_hora=m.data_hora,
                ip=m.ip
            ) for m in LogAcaoModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove o Log_acao com a PK informada.
        """
        LogAcaoModel.objects.filter(pk=id).delete()
