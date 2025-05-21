from abc import ABC, abstractmethod
from typing import List
from core.application.dtos.area_dto import CreateAreaDTO, AreaDTO

class IAreaService(ABC):
    @abstractmethod
    def create(self, input: CreateAreaDTO) -> AreaDTO: ...
    @abstractmethod
    def find_by_id(self, id: int) -> AreaDTO: ...
    @abstractmethod
    def list_all(self) -> List[AreaDTO]: ...
