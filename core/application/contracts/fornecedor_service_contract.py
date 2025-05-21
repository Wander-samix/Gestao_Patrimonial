# core/application/contracts/fornecedor_service_contract.py
from abc import ABC, abstractmethod
from typing import List, Optional
from core.application.dtos.fornecedor_dto import (
    CreateFornecedorDTO,
    FornecedorDTO
)

class IFornecedorService(ABC):
    @abstractmethod
    def create(self, dto: CreateFornecedorDTO) -> FornecedorDTO:
        """Cria um novo fornecedor a partir de um DTO de entrada."""
        ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[FornecedorDTO]:
        """Retorna um fornecedor pelo ID, ou None se não existir."""
        ...

    @abstractmethod
    def list_all(self) -> List[FornecedorDTO]:
        """Retorna todos os fornecedores."""
        ...
