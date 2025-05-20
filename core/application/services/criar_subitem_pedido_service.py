from typing import Dict, Any, Optional

from core.domain.entities.subitem_pedido import Subitem_pedido
from core.domain.repositories.subitem_pedido_repository import ISubitem_pedidoRepository
from infrastructure.repositories.django_subitem_pedido_repository import DjangoSubitem_pedidoRepository

class CriarSubitem_pedidoService:
    def __init__(self, repo: ISubitem_pedidoRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoSubitem_pedidoRepository()

    def execute(self, dados: Dict[str, Any]) -> Subitem_pedido:
        """
        dados esperados:
          - pedido_id: int (obrigatório, >0)
          - produto_id: int (obrigatório, >0)
          - quantidade: int (obrigatório, >0)
          - estoque_no_pedido: int (opcional, >=0)
        Retorna a entidade Subitem_pedido recém-criada.
        """
        # valida pedido_id
        pedido_id = dados.get('pedido_id')
        if not isinstance(pedido_id, int) or pedido_id < 1:
            raise ValueError("O campo 'pedido_id' é obrigatório e deve ser um inteiro positivo.")

        # valida produto_id
        produto_id = dados.get('produto_id')
        if not isinstance(produto_id, int) or produto_id < 1:
            raise ValueError("O campo 'produto_id' é obrigatório e deve ser um inteiro positivo.")

        # valida quantidade
        quantidade = dados.get('quantidade')
        if not isinstance(quantidade, int) or quantidade < 1:
            raise ValueError("O campo 'quantidade' é obrigatório e deve ser um inteiro maior que zero.")

        # valida estoque_no_pedido (opcional)
        estoque_no_pedido: Optional[int] = dados.get('estoque_no_pedido')
        if estoque_no_pedido is not None:
            if not isinstance(estoque_no_pedido, int) or estoque_no_pedido < 0:
                raise ValueError("Se informado, 'estoque_no_pedido' deve ser um inteiro >= 0.")

        # monta a entidade de domínio
        subitem = Subitem_pedido(
            pedido_id=pedido_id,
            produto_id=produto_id,
            quantidade=quantidade,
            estoque_no_pedido=estoque_no_pedido
        )

        # persiste e retorna
        return self.repo.save(subitem)
