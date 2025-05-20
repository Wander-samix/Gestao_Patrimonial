from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.subitem_pedido import Subitem_pedido

class ISubitem_pedidoRepository(ABC):
    @abstractmethod
    def save(self, obj: Subitem_pedido) -> Subitem_pedido: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Subitem_pedido]: ...

    @abstractmethod
    def list_all(self) -> List[Subitem_pedido]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
