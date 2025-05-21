from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.movimentacao_estoque import MovimentacaoEstoque

class IMovimentacaoEstoqueRepository(ABC):
    @abstractmethod
    def save(self, obj: MovimentacaoEstoque) -> MovimentacaoEstoque: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[MovimentacaoEstoque]: ...

    @abstractmethod
    def list_all(self) -> List[MovimentacaoEstoque]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
