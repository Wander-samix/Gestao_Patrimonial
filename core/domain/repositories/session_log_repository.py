from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.session_log import SessionLog

class ISessionLogRepository(ABC):
    @abstractmethod
    def save(self, obj: SessionLog) -> SessionLog: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[SessionLog]: ...

    @abstractmethod
    def list_all(self) -> List[SessionLog]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
