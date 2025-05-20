from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.saida_produto_por_pedido import Saida_produto_por_pedido

class ISaida_produto_por_pedidoRepository(ABC):
    @abstractmethod
    def save(self, obj: Saida_produto_por_pedido) -> Saida_produto_por_pedido: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Saida_produto_por_pedido]: ...

    @abstractmethod
    def list_all(self) -> List[Saida_produto_por_pedido]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
