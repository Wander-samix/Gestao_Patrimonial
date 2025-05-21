from abc import ABC, abstractmethod
from core.application.dtos.configuracao_estoque_dto import (
    CreateConfiguracaoEstoqueDTO,
    ConfiguracaoEstoqueDTO,
)

class IConfiguracaoEstoqueService(ABC):
    @abstractmethod
    def create(self, dto: CreateConfiguracaoEstoqueDTO) -> ConfiguracaoEstoqueDTO:
        """
        Cria ou atualiza uma ConfiguracaoEstoque a partir do DTO de entrada
        e retorna sempre um DTO de saída.
        """
        ...
