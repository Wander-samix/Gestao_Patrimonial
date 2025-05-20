from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.pedido import Pedido

class IPedidoRepository(ABC):
    @abstractmethod
    def save(self, obj: Pedido) -> Pedido: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Pedido]: ...

    @abstractmethod
    def list_all(self) -> List[Pedido]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
