from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.log_acao import Log_acao

class ILog_acaoRepository(ABC):
    @abstractmethod
    def save(self, obj: Log_acao) -> Log_acao: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Log_acao]: ...

    @abstractmethod
    def list_all(self) -> List[Log_acao]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
