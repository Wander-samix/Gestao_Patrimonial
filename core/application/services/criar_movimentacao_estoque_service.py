from datetime import datetime
from typing import Optional
import ipaddress

from core.application.contracts.movimentacao_estoque_service_contract import IMovimentacaoEstoqueService
from core.application.dtos.movimentacao_estoque_dto import (
    CreateMovimentacaoEstoqueDTO,
    MovimentacaoEstoqueDTO,
)
from core.domain.entities.movimentacao_estoque import MovimentacaoEstoque
from core.domain.repositories.movimentacao_estoque_repository import IMovimentacaoEstoqueRepository
from infrastructure.repositories.django_movimentacao_estoque_repository import DjangoMovimentacaoEstoqueRepository

class MovimentacaoEstoqueService(IMovimentacaoEstoqueService):
    def __init__(self, repo: IMovimentacaoEstoqueRepository = None):
        self.repo = repo or DjangoMovimentacaoEstoqueRepository()

    def create(self, dto: CreateMovimentacaoEstoqueDTO) -> MovimentacaoEstoqueDTO:
        # tipo
        if dto.tipo not in ("entrada", "saida"):
            raise ValueError("O campo 'tipo' deve ser 'entrada' ou 'saida'.")

        # data
        data = dto.data
        if data is None:
            data = datetime.now()
        elif not isinstance(data, datetime):
            raise ValueError("'data' deve ser um datetime, se informado.")

        # usuario_id
        if not isinstance(dto.usuario_id, int) or dto.usuario_id < 1:
            raise ValueError("O campo 'usuario_id' deve ser inteiro positivo.")

        # quantidade
        if not isinstance(dto.quantidade, int) or dto.quantidade <= 0:
            raise ValueError("O campo 'quantidade' deve ser inteiro > 0.")

        # produto_id
        if not isinstance(dto.produto_id, int) or dto.produto_id < 1:
            raise ValueError("O campo 'produto_id' deve ser inteiro positivo.")

        # nota_fiscal_id
        if dto.nota_fiscal_id is not None:
            if not isinstance(dto.nota_fiscal_id, int) or dto.nota_fiscal_id < 1:
                raise ValueError("'nota_fiscal_id' deve ser inteiro positivo, se informado.")

        # cliente_id
        if dto.cliente_id is not None:
            if not isinstance(dto.cliente_id, int) or dto.cliente_id < 1:
                raise ValueError("'cliente_id' deve ser inteiro positivo, se informado.")

        # monta entidade e persiste
        mov = Movimentacao_estoque(
            tipo=dto.tipo,
            data=data,
            usuario_id=dto.usuario_id,
            quantidade=dto.quantidade,
            produto_id=dto.produto_id,
            nota_fiscal_id=dto.nota_fiscal_id,
            cliente_id=dto.cliente_id,
        )
        criado = self.repo.save(mov)

        return MovimentacaoEstoqueDTO(
            id=criado.id,
            tipo=criado.tipo,
            data=criado.data,
            usuario_id=criado.usuario_id,
            quantidade=criado.quantidade,
            produto_id=criado.produto_id,
            nota_fiscal_id=criado.nota_fiscal_id,
            cliente_id=criado.cliente_id,
        )
