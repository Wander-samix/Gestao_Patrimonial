from abc import ABC, abstractmethod
from core.application.dtos.log_acao_dto import CreateLogAcaoDTO, LogAcaoDTO

class ILogAcaoService(ABC):
    @abstractmethod
    def create(self, dto: CreateLogAcaoDTO) -> LogAcaoDTO:
        """Cria um LogAcao e retorna seus dados em um DTO."""
        ...
