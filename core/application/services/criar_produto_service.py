from typing import Dict, Any, Optional
from datetime import date
from decimal import Decimal, InvalidOperation

from core.domain.entities.produto import Produto
from core.domain.repositories.produto_repository import IProdutoRepository
from infrastructure.repositories.django_produto_repository import DjangoProdutoRepository

class CriarProdutoService:
    def __init__(self, repo: IProdutoRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoProdutoRepository()

    def execute(self, dados: Dict[str, Any]) -> Produto:
        """
        dados esperados:
          - codigo_barras: str (obrigatório, max_length=100)
          - descricao: str (obrigatório, max_length=255)
          - fornecedor_id: int (obrigatório, >0)
          - quantidade: int (obrigatório, >=0)
          - preco_unitario: Decimal ou float (opcional, >=0, default 0)
          - nfe_numero: str (opcional, max_length=20)
          - area_id: int (opcional, >0)
          - validade: date (opcional)
        Retorna a entidade Produto recém-criada.
        """
        # valida codigo_barras
        codigo_barras = dados.get('codigo_barras')
        if not codigo_barras or not isinstance(codigo_barras, str) or not codigo_barras.strip():
            raise ValueError("O campo 'codigo_barras' é obrigatório e não pode ser vazio.")
        codigo_barras = codigo_barras.strip()[:100]

        # valida descricao
        descricao = dados.get('descricao')
        if not descricao or not isinstance(descricao, str) or not descricao.strip():
            raise ValueError("O campo 'descricao' é obrigatório e não pode ser vazio.")
        descricao = descricao.strip()[:255]

        # valida fornecedor_id
        fornecedor_id = dados.get('fornecedor_id')
        if not isinstance(fornecedor_id, int) or fornecedor_id < 1:
            raise ValueError("O campo 'fornecedor_id' é obrigatório e deve ser um inteiro positivo.")

        # valida quantidade
        quantidade = dados.get('quantidade')
        if not isinstance(quantidade, int) or quantidade < 0:
            raise ValueError("O campo 'quantidade' é obrigatório e deve ser um inteiro >= 0.")

        # valida preco_unitario
        preco_raw = dados.get('preco_unitario', 0)
        try:
            preco_unitario = Decimal(preco_raw)
        except (InvalidOperation, TypeError):
            raise ValueError("'preco_unitario' deve ser um número válido.")
        if preco_unitario < 0:
            raise ValueError("'preco_unitario' deve ser maior ou igual a zero.")

        # valida nfe_numero (opcional)
        nfe_numero = dados.get('nfe_numero')
        if nfe_numero is not None:
            if not isinstance(nfe_numero, str):
                raise ValueError("'nfe_numero' deve ser uma string.")
            nfe_numero = nfe_numero.strip()[:20] or None

        # valida area_id (opcional)
        area_id: Optional[int] = dados.get('area_id')
        if area_id is not None:
            if not isinstance(area_id, int) or area_id < 1:
                raise ValueError("'area_id' deve ser um inteiro positivo, se informado.")

        # valida validade (opcional)
        validade: Optional[date] = dados.get('validade')
        if validade is not None and not isinstance(validade, date):
            raise ValueError("'validade' deve ser um objeto date, se informado.")

        # monta a entidade de domínio
        produto = Produto(
            codigo_barras=codigo_barras,
            descricao=descricao,
            fornecedor_id=fornecedor_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            nfe_numero=nfe_numero,
            area_id=area_id,
            validade=validade
        )

        # persiste e retorna
        return self.repo.save(produto)
