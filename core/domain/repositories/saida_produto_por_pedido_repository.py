from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.saida_produto_por_pedido import SaidaProdutoPorPedido

class ISaidaProdutoPorPedidoRepository(ABC):
    @abstractmethod
    def save(self, obj: SaidaProdutoPorPedido) -> SaidaProdutoPorPedido: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[SaidaProdutoPorPedido]: ...

    @abstractmethod
    def list_all(self) -> List[SaidaProdutoPorPedido]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
