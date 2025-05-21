from core.application.contracts.subitem_pedido_service_contract import ISubitemPedidoService
from core.application.dtos.subitem_pedido_dto import CreateSubitemPedidoDTO, SubitemPedidoDTO
from core.domain.entities.subitem_pedido import Subitem_pedido
from core.domain.repositories.subitem_pedido_repository import ISubitem_pedidoRepository
from infrastructure.repositories.django_subitem_pedido_repository import DjangoSubitem_pedidoRepository

class SubitemPedidoService(ISubitemPedidoService):
    def __init__(self, repo: ISubitem_pedidoRepository = None):
        self.repo = repo or DjangoSubitem_pedidoRepository()

    def create(self, dto: CreateSubitemPedidoDTO) -> SubitemPedidoDTO:
        # validações simples (já estão no domínio, mas podemos reforçar aqui)
        if dto.pedido_id < 1:
            raise ValueError("`pedido_id` deve ser inteiro positivo.")
        if dto.produto_id < 1:
            raise ValueError("`produto_id` deve ser inteiro positivo.")
        if dto.quantidade < 1:
            raise ValueError("`quantidade` deve ser maior que zero.")
        if dto.estoque_no_pedido is not None and dto.estoque_no_pedido < 0:
            raise ValueError("`estoque_no_pedido` deve ser >= 0, se informado.")

        # monta a entidade de domínio
        entidade = Subitem_pedido(
            pedido_id=dto.pedido_id,
            produto_id=dto.produto_id,
            quantidade=dto.quantidade,
            estoque_no_pedido=dto.estoque_no_pedido,
        )
        salvo = self.repo.save(entidade)

        # retorna DTO de saída
        return SubitemPedidoDTO(
            id=salvo.id,
            pedido_id=salvo.pedido_id,
            produto_id=salvo.produto_id,
            quantidade=salvo.quantidade,
            estoque_no_pedido=salvo.estoque_no_pedido,
        )
