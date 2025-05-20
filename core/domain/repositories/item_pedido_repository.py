from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.item_pedido import Item_pedido

class IItem_pedidoRepository(ABC):
    @abstractmethod
    def save(self, obj: Item_pedido) -> Item_pedido: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Item_pedido]: ...

    @abstractmethod
    def list_all(self) -> List[Item_pedido]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
