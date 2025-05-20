from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.configuracao_estoque import Configuracao_estoque

class IConfiguracao_estoqueRepository(ABC):
    @abstractmethod
    def save(self, obj: Configuracao_estoque) -> Configuracao_estoque: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Configuracao_estoque]: ...

    @abstractmethod
    def list_all(self) -> List[Configuracao_estoque]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
