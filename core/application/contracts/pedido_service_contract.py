from abc import ABC, abstractmethod
from core.application.dtos.pedido_dto import CreatePedidoDTO, PedidoDTO

class IPedidoService(ABC):
    @abstractmethod
    def create(self, dto: CreatePedidoDTO) -> PedidoDTO:
        """
        Cria um Pedido e retorna seus dados em um DTO.
        """
        ...
