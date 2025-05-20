from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.usuario import Usuario

class IUsuarioRepository(ABC):
    @abstractmethod
    def save(self, obj: Usuario) -> Usuario: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Usuario]: ...

    @abstractmethod
    def list_all(self) -> List[Usuario]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...
