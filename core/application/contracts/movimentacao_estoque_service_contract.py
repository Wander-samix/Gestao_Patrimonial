from abc import ABC, abstractmethod
from core.application.dtos.movimentacao_estoque_dto import (
    CreateMovimentacaoEstoqueDTO,
    MovimentacaoEstoqueDTO,
)

class IMovimentacaoEstoqueService(ABC):
    @abstractmethod
    def create(self, dto: CreateMovimentacaoEstoqueDTO) -> MovimentacaoEstoqueDTO:
        """
        Cria uma movimentação de estoque e retorna seus dados em um DTO.
        """
        ...
