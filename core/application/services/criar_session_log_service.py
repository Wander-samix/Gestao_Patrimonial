from datetime import datetime
from core.application.contracts.session_log_service_contract import ISessionLogService
from core.application.dtos.session_log_dto import CreateSessionLogDTO, SessionLogDTO
from core.domain.entities.session_log import Session_log
from core.domain.repositories.session_log_repository import ISession_logRepository
from infrastructure.repositories.django_session_log_repository import DjangoSession_logRepository

class SessionLogService(ISessionLogService):
    def __init__(self, repo: ISession_logRepository = None):
        self.repo = repo or DjangoSession_logRepository()

    def create(self, dto: CreateSessionLogDTO) -> SessionLogDTO:
        # validações básicas
        if dto.user_id < 1:
            raise ValueError("`user_id` deve ser inteiro positivo.")
        if not dto.session_key.strip():
            raise ValueError("`session_key` não pode ser vazio.")
        if not isinstance(dto.login_time, datetime):
            raise ValueError("`login_time` deve ser datetime.")

        # se informaram logout_time, deve ser >= login_time
        if dto.logout_time and dto.logout_time < dto.login_time:
            raise ValueError("`logout_time` não pode ser anterior a `login_time`.")

        entidade = Session_log(
            user_id=dto.user_id,
            session_key=dto.session_key,
            login_time=dto.login_time,
            logout_time=dto.logout_time,
            duration=dto.duration,
            ip=dto.ip,
        )
        salvo = self.repo.save(entidade)

        return SessionLogDTO(
            id=salvo.id,
            user_id=salvo.user_id,
            session_key=salvo.session_key,
            login_time=salvo.login_time.isoformat(),
            logout_time=salvo.logout_time and salvo.logout_time.isoformat(),
            duration=salvo.duration.total_seconds() if salvo.duration else None,
            ip=salvo.ip,
        )
