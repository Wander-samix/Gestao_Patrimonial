from datetime import datetime

from core.application.contracts.saida_produto_por_pedido_service_contract import (
    ISaidaProdutoPorPedidoService,
)
from core.application.dtos.saida_produto_por_pedido_dto import (
    CreateSaidaProdutoPorPedidoDTO,
    SaidaProdutoPorPedidoDTO,
)
from core.domain.entities.saida_produto_por_pedido import Saida_produto_por_pedido
from core.domain.repositories.saida_produto_por_pedido_repository import (
    ISaida_produto_por_pedidoRepository,
)
from infrastructure.repositories.django_saida_produto_por_pedido_repository import (
    DjangoSaida_produto_por_pedidoRepository,
)

class SaidaProdutoPorPedidoService(ISaidaProdutoPorPedidoService):
    def __init__(self, repo: ISaida_produto_por_pedidoRepository = None):
        self.repo = repo or DjangoSaida_produto_por_pedidoRepository()

    def create(self, dto: CreateSaidaProdutoPorPedidoDTO) -> SaidaProdutoPorPedidoDTO:
        # validações
        if dto.produto_id < 1:
            raise ValueError("`produto_id` deve ser inteiro positivo.")
        if dto.pedido_id < 1:
            raise ValueError("`pedido_id` deve ser inteiro positivo.")
        if dto.quantidade < 1:
            raise ValueError("`quantidade` deve ser maior que zero.")

        # monta entidade de domínio
        entidade = Saida_produto_por_pedido(
            produto_id=dto.produto_id,
            pedido_id=dto.pedido_id,
            quantidade=dto.quantidade
        )
        salvo = self.repo.save(entidade)

        return SaidaProdutoPorPedidoDTO(
            id=salvo.id,
            produto_id=salvo.produto_id,
            pedido_id=salvo.pedido_id,
            quantidade=salvo.quantidade,
            data_saida=salvo.data_saida.isoformat(),
        )
