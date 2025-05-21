from abc import ABC, abstractmethod
from core.application.dtos.saida_produto_por_pedido_dto import (
    CreateSaidaProdutoPorPedidoDTO,
    SaidaProdutoPorPedidoDTO,
)

class ISaidaProdutoPorPedidoService(ABC):
    @abstractmethod
    def create(self, dto: CreateSaidaProdutoPorPedidoDTO) -> SaidaProdutoPorPedidoDTO:
        """
        Registra uma saída de produto por pedido e retorna os dados em um DTO.
        """
        ...
