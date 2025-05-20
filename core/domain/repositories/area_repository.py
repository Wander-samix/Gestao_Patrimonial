# core/domain/repositories/area_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.area import Area

class IAreaRepository(ABC):
    @abstractmethod
    def save(self, obj: Area) -> Area: ...
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Area]: ...
    @abstractmethod
    def list_all(self) -> List[Area]: ...
    @abstractmethod
    def delete(self, id: int) -> None: ...
