from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.item_pedido import ItemPedido

class IItemPedidoRepository(ABC):
    @abstractmethod
    def save(self, obj: ItemPedido) -> ItemPedido: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[ItemPedido]: ...

    @abstractmethod
    def list_all(self) -> List[ItemPedido]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
