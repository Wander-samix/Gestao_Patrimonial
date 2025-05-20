from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.movimentacao_estoque import Movimentacao_estoque

class IMovimentacao_estoqueRepository(ABC):
    @abstractmethod
    def save(self, obj: Movimentacao_estoque) -> Movimentacao_estoque: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Movimentacao_estoque]: ...

    @abstractmethod
    def list_all(self) -> List[Movimentacao_estoque]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
