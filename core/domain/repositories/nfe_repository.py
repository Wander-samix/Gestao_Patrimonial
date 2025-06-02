# core/domain/repositories/nfe_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.nfe import Nfe

class INfeRepository(ABC):
    @abstractmethod
    def save(self, obj: Nfe) -> Nfe: ...
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Nfe]: ...
    @abstractmethod
    def list_all(self) -> List[Nfe]: ...
    @abstractmethod
    def delete(self, id: int) -> None: ...
