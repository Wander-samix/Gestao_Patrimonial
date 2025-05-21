from abc import ABC, abstractmethod
from core.application.dtos.subitem_pedido_dto import CreateSubitemPedidoDTO, SubitemPedidoDTO

class ISubitemPedidoService(ABC):

    @abstractmethod
    def create(self, dto: CreateSubitemPedidoDTO) -> SubitemPedidoDTO:
        """
        Cria um Subitem_pedido a partir do DTO e devolve seus dados em um DTO de saída.
        """
        ...
