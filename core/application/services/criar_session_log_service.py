from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import ipaddress

from core.domain.entities.session_log import Session_log
from core.domain.repositories.session_log_repository import ISession_logRepository
from infrastructure.repositories.django_session_log_repository import DjangoSession_logRepository

class CriarSession_logService:
    def __init__(self, repo: ISession_logRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoSession_logRepository()

    def execute(self, dados: Dict[str, Any]) -> Session_log:
        """
        dados esperados:
          - user_id: int (obrigatório, >0)
          - session_key: str (obrigatório, não vazio, max_length=40)
          - login_time: datetime (obrigatório)
          - logout_time: datetime (opcional, >= login_time)
          - duration: timedelta (opcional)
          - ip: str (opcional, formato IPv4/IPv6)
        Retorna a entidade Session_log recém-criada.
        """
        # valida user_id
        user_id = dados.get('user_id')
        if not isinstance(user_id, int) or user_id < 1:
            raise ValueError("O campo 'user_id' é obrigatório e deve ser um inteiro positivo.")

        # valida session_key
        session_key = dados.get('session_key')
        if not session_key or not isinstance(session_key, str) or not session_key.strip():
            raise ValueError("O campo 'session_key' é obrigatório e não pode ser vazio.")
        session_key = session_key.strip()[:40]

        # valida login_time
        login_time = dados.get('login_time')
        if not isinstance(login_time, datetime):
            raise ValueError("O campo 'login_time' é obrigatório e deve ser um objeto datetime.")

        # valida logout_time (opcional)
        logout_time: Optional[datetime] = dados.get('logout_time')
        if logout_time is not None:
            if not isinstance(logout_time, datetime):
                raise ValueError("'logout_time' deve ser um objeto datetime, se informado.")
            if logout_time < login_time:
                raise ValueError("'logout_time' não pode ser anterior a 'login_time'.")

        # valida duration (opcional)
        duration: Optional[timedelta] = dados.get('duration')
        if duration is not None and not isinstance(duration, timedelta):
            raise ValueError("'duration' deve ser um objeto timedelta, se informado.")

        # valida ip (opcional)
        ip: Optional[str] = dados.get('ip')
        if ip is not None:
            if not isinstance(ip, str):
                raise ValueError("'ip' deve ser uma string.")
            ip = ip.strip()
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                raise ValueError(f"'{ip}' não é um endereço IP válido.")

        # monta a entidade de domínio
        session_log = Session_log(
            user_id=user_id,
            session_key=session_key,
            login_time=login_time,
            logout_time=logout_time,
            duration=duration,
            ip=ip
        )

        # persiste e retorna
        return self.repo.save(session_log)
