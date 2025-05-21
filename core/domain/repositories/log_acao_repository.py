from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.log_acao import LogAcao

class ILogAcaoRepository(ABC):
    @abstractmethod
    def save(self, obj: LogAcao) -> LogAcao: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[LogAcao]: ...

    @abstractmethod
    def list_all(self) -> List[LogAcao]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
