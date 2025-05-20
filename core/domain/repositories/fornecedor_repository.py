from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.fornecedor import Fornecedor

class IFornecedorRepository(ABC):
    @abstractmethod
    def save(self, obj: Fornecedor) -> Fornecedor: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Fornecedor]: ...

    @abstractmethod
    def list_all(self) -> List[Fornecedor]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
