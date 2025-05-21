from abc import ABC, abstractmethod
from core.application.dtos.item_pedido_dto import CreateItemPedidoDTO, ItemPedidoDTO

class IItemPedidoService(ABC):
    @abstractmethod
    def create(self, dto: CreateItemPedidoDTO) -> ItemPedidoDTO:
        """Cria um ItemPedido e retorna seus dados em um DTO."""
        ...
