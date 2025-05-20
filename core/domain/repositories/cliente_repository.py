from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.cliente import Cliente

class IClienteRepository(ABC):
    @abstractmethod
    def save(self, obj: Cliente) -> Cliente: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Cliente]: ...

    @abstractmethod
    def list_all(self) -> List[Cliente]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
