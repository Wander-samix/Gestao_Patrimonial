from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.session_log import Session_log

class ISession_logRepository(ABC):
    @abstractmethod
    def save(self, obj: Session_log) -> Session_log: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Session_log]: ...

    @abstractmethod
    def list_all(self) -> List[Session_log]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
