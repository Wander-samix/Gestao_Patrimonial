from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Optional

from core.application.contracts.produto_service_contract import IProdutoService
from core.application.dtos.produto_dto import CreateProdutoDTO, ProdutoDTO
from core.domain.entities.produto import Produto
from core.domain.repositories.produto_repository import IProdutoRepository
from infrastructure.repositories.django_produto_repository import DjangoProdutoRepository

class ProdutoService(IProdutoService):
    def __init__(self, repo: IProdutoRepository = None):
        self.repo = repo or DjangoProdutoRepository()

    def create(self, dto: CreateProdutoDTO) -> ProdutoDTO:
        # Validações (pode extrair p/ métodos auxiliares)
        if not dto.codigo_barras.strip():
            raise ValueError("`codigo_barras` é obrigatório.")
        dto.codigo_barras = dto.codigo_barras.strip()[:100]

        if not dto.descricao.strip():
            raise ValueError("`descricao` é obrigatório.")
        dto.descricao = dto.descricao.strip()[:255]

        if dto.fornecedor_id < 1:
            raise ValueError("`fornecedor_id` deve ser inteiro positivo.")

        if dto.quantidade < 0:
            raise ValueError("`quantidade` deve ser >= 0.")

        try:
            preco = Decimal(dto.preco_unitario)
        except (InvalidOperation, TypeError):
            raise ValueError("`preco_unitario` inválido.")
        if preco < 0:
            raise ValueError("`preco_unitario` deve ser >= 0.")
        dto.preco_unitario = preco

        if dto.nfe_numero is not None:
            dto.nfe_numero = dto.nfe_numero.strip()[:20] or None

        if dto.area_id is not None and dto.area_id < 1:
            raise ValueError("`area_id` deve ser inteiro positivo se informado.")

        if dto.validade is not None and not isinstance(dto.validade, date):
            raise ValueError("`validade` deve ser date.")

        # Monta entidade
        produto = Produto(
            codigo_barras=dto.codigo_barras,
            descricao=dto.descricao,
            fornecedor_id=dto.fornecedor_id,
            quantidade=dto.quantidade,
            preco_unitario=dto.preco_unitario,
            nfe_numero=dto.nfe_numero,
            area_id=dto.area_id,
            validade=dto.validade
        )
        criado = self.repo.save(produto)

        return ProdutoDTO(
            id=criado.id,
            codigo_barras=criado.codigo_barras,
            descricao=criado.descricao,
            fornecedor_id=criado.fornecedor_id,
            quantidade=criado.quantidade,
            preco_unitario=criado.preco_unitario,
            nfe_numero=criado.nfe_numero,
            area_id=criado.area_id,
            validade=criado.validade,
            lote=criado.lote,
            criado_em=criado.criado_em.date(),
        )
