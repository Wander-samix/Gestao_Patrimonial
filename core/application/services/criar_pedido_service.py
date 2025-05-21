from datetime import date
from typing import Optional

from core.application.contracts.pedido_service_contract import IPedidoService
from core.application.dtos.pedido_dto import CreatePedidoDTO, PedidoDTO
from core.domain.entities.pedido import Pedido
from core.domain.repositories.pedido_repository import IPedidoRepository
from infrastructure.repositories.django_pedido_repository import DjangoPedidoRepository

class PedidoService(IPedidoService):
    def __init__(self, repo: IPedidoRepository = None):
        self.repo = repo or DjangoPedidoRepository()

    def create(self, dto: CreatePedidoDTO) -> PedidoDTO:
        # valida codigo
        codigo = dto.codigo.strip()
        if not codigo:
            raise ValueError("O campo 'codigo' é obrigatório e não pode ser vazio.")
        codigo = codigo[:20]

        # valida usuario_id
        if not isinstance(dto.usuario_id, int) or dto.usuario_id < 1:
            raise ValueError("O campo 'usuario_id' é obrigatório e deve ser um inteiro positivo.")

        # valida data_necessaria
        data_necessaria: Optional[date] = dto.data_necessaria
        if data_necessaria is not None and not isinstance(data_necessaria, date):
            raise ValueError("'data_necessaria' deve ser um objeto date, se informado.")

        # valida observacao
        observacao: Optional[str] = dto.observacao
        if observacao is not None:
            if not isinstance(observacao, str):
                raise ValueError("'observacao' deve ser uma string.")
            observacao = observacao.strip()

        # monta a entidade
        pedido = Pedido(
            codigo=codigo,
            usuario_id=dto.usuario_id,
            data_necessaria=data_necessaria,
            observacao=observacao
        )
        criado = self.repo.save(pedido)

        return PedidoDTO(
            id=criado.id,
            codigo=criado.codigo,
            usuario_id=criado.usuario_id,
            data_solicitacao=criado.data_solicitacao.date(),
            status=criado.status,
            data_necessaria=criado.data_necessaria,
            observacao=criado.observacao,
        )
