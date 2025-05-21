# core/application/contracts/cliente_service_contract.py
from abc import ABC, abstractmethod
from typing import List
from core.application.dtos.cliente_dto import (
    CreateClienteDTO,
    ClienteDTO
)

class IClienteService(ABC):
    @abstractmethod
    def create(self, dto: CreateClienteDTO) -> ClienteDTO:
        ...

    @abstractmethod
    def find_by_id(self, id: int) -> ClienteDTO:
        ...

    @abstractmethod
    def list_all(self) -> List[ClienteDTO]:
        ...
