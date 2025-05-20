from typing import Dict, Any, Optional
from datetime import datetime
from core.domain.entities.movimentacao_estoque import Movimentacao_estoque
from core.domain.repositories.movimentacao_estoque_repository import IMovimentacao_estoqueRepository
from infrastructure.repositories.django_movimentacao_estoque_repository import DjangoMovimentacao_estoqueRepository

class CriarMovimentacao_estoqueService:
    def __init__(self, repo: IMovimentacao_estoqueRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoMovimentacao_estoqueRepository()

    def execute(self, dados: Dict[str, Any]) -> Movimentacao_estoque:
        """
        dados esperados:
          - tipo: str ("entrada" ou "saida", obrigatório)
          - data: datetime (opcional, default agora)
          - usuario_id: int (obrigatório, >0)
          - quantidade: int (obrigatório, >0)
          - produto_id: int (obrigatório, >0)
          - nota_fiscal_id: int (opcional, >0)
          - cliente_id: int (opcional, >0)
        Retorna a entidade Movimentacao_estoque recém-criada.
        """
        # valida tipo
        tipo = dados.get('tipo')
        if tipo not in ('entrada', 'saida'):
            raise ValueError("O campo 'tipo' é obrigatório e deve ser 'entrada' ou 'saida'.")

        # data (opcional)
        data = dados.get('data')
        if data is not None:
            if not isinstance(data, datetime):
                raise ValueError("'data' deve ser um objeto datetime.")
        else:
            data = datetime.now()

        # usuario_id
        usuario_id = dados.get('usuario_id')
        if not isinstance(usuario_id, int) or usuario_id < 1:
            raise ValueError("O campo 'usuario_id' é obrigatório e deve ser um inteiro positivo.")

        # quantidade
        quantidade = dados.get('quantidade')
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("O campo 'quantidade' é obrigatório e deve ser um inteiro maior que zero.")

        # produto_id
        produto_id = dados.get('produto_id')
        if not isinstance(produto_id, int) or produto_id < 1:
            raise ValueError("O campo 'produto_id' é obrigatório e deve ser um inteiro positivo.")

        # nota_fiscal_id (opcional)
        nota_fiscal_id: Optional[int] = dados.get('nota_fiscal_id')
        if nota_fiscal_id is not None:
            if not isinstance(nota_fiscal_id, int) or nota_fiscal_id < 1:
                raise ValueError("'nota_fiscal_id' deve ser um inteiro positivo, se informado.")

        # cliente_id (opcional)
        cliente_id: Optional[int] = dados.get('cliente_id')
        if cliente_id is not None:
            if not isinstance(cliente_id, int) or cliente_id < 1:
                raise ValueError("'cliente_id' deve ser um inteiro positivo, se informado.")

        # monta a entidade de domínio
        mov = Movimentacao_estoque(
            tipo=tipo,
            data=data,
            usuario_id=usuario_id,
            quantidade=quantidade,
            produto_id=produto_id,
            nota_fiscal_id=nota_fiscal_id,
            cliente_id=cliente_id
        )
        # persiste e retorna
        return self.repo.save(mov)
