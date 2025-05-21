from abc import ABC, abstractmethod
from core.application.dtos.session_log_dto import (
    CreateSessionLogDTO,
    SessionLogDTO,
)

class ISessionLogService(ABC):

    @abstractmethod
    def create(self, dto: CreateSessionLogDTO) -> SessionLogDTO:
        """
        Registra um log de sessão e retorna seus dados em um DTO.
        """
        ...
