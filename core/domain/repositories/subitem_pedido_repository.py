from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.subitem_pedido import SubItemPedido

class ISubItemPedidoRepository(ABC):
    @abstractmethod
    def save(self, obj: SubItemPedido) -> SubItemPedido: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[SubItemPedido]: ...

    @abstractmethod
    def list_all(self) -> List[SubItemPedido]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
