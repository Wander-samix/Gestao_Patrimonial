from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.produto import Produto

class IProdutoRepository(ABC):
    @abstractmethod
    def save(self, obj: Produto) -> Produto: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Produto]: ...

    @abstractmethod
    def list_all(self) -> List[Produto]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
