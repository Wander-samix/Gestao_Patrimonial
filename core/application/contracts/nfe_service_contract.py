from abc import ABC, abstractmethod
from core.application.dtos.nfe_dto import CreateNfeDTO, NfeDTO

class INfeService(ABC):
    @abstractmethod
    def create(self, dto: CreateNfeDTO) -> NfeDTO:
        """
        Cria uma NFe e retorna seus dados em um DTO.
        """
        ...
