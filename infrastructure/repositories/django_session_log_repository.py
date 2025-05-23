from typing import List, Optional
from core.domain.entities.session_log import SessionLog
from core.domain.repositories.session_log_repository import ISessionLogRepository
from core.models import SessionLog as SessionLogModel

class DjangoSessionLogRepository(ISessionLogRepository):
    def save(self, obj: SessionLog) -> SessionLog:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Retorna a entidade de domínio com o id gerado/atualizado.
        """
        if getattr(obj, 'id', None):
            m = SessionLogModel.objects.get(pk=obj.id)
            m.user_id     = obj.user_id
            m.session_key = obj.session_key
            m.login_time  = obj.login_time
            m.logout_time = obj.logout_time
            m.duration    = obj.duration
            m.ip          = obj.ip
            m.save(update_fields=[
                'user', 'session_key', 'login_time',
                'logout_time', 'duration', 'ip'
            ])
        else:
            m = SessionLogModel.objects.create(
                user_id     = obj.user_id,
                session_key = obj.session_key,
                login_time  = obj.login_time,
                logout_time = obj.logout_time,
                duration    = obj.duration,
                ip          = obj.ip
            )
        return SessionLog(
            id=m.id,
            user_id=m.user_id,
            session_key=m.session_key,
            login_time=m.login_time,
            logout_time=m.logout_time,
            duration=m.duration,
            ip=m.ip
        )

    def find_by_id(self, id: int) -> Optional[SessionLog]:
        """
        Busca SessionLog por PK; retorna None se não existir.
        """
        try:
            m = SessionLogModel.objects.get(pk=id)
            return SessionLog(
                id=m.id,
                user_id=m.user_id,
                session_key=m.session_key,
                login_time=m.login_time,
                logout_time=m.logout_time,
                duration=m.duration,
                ip=m.ip
            )
        except SessionLogModel.DoesNotExist:
            return None

    def list_all(self) -> List[SessionLog]:
        """
        Retorna todos os SessionLog como entidades de domínio.
        """
        return [
            SessionLog(
                id=m.id,
                user_id=m.user_id,
                session_key=m.session_key,
                login_time=m.login_time,
                logout_time=m.logout_time,
                duration=m.duration,
                ip=m.ip
            )
            for m in SessionLogModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove o Session_log com a PK informada.
        """
        SessionLogModel.objects.filter(pk=id).delete()
