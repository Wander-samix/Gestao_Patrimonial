from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.configuracao_estoque import ConfiguracaoEstoque
from core.domain.repositories.configuracao_estoque_repository import IConfiguracaoEstoqueRepository
from core.models import ConfiguracaoEstoque as ConfiguracaoEstoqueModel

class IConfiguracaoEstoqueRepository(IConfiguracaoEstoqueRepository):
    @abstractmethod
    def save(self, obj: ConfiguracaoEstoque) -> ConfiguracaoEstoque: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[ConfiguracaoEstoque]: ...

    @abstractmethod
    def list_all(self) -> List[ConfiguracaoEstoque]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
