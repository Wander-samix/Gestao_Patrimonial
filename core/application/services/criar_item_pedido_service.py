from typing import Dict, Any
from core.domain.entities.item_pedido import Item_pedido
from core.domain.repositories.item_pedido_repository import IItem_pedidoRepository
from infrastructure.repositories.django_item_pedido_repository import DjangoItem_pedidoRepository

class CriarItem_pedidoService:
    def __init__(self, repo: IItem_pedidoRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoItem_pedidoRepository()

    def execute(self, dados: Dict[str, Any]) -> Item_pedido:
        """
        dados esperados:
          - pedido_id: int (obrigatório, >0)
          - produto_id: int (obrigatório, >0)
          - quantidade: int (obrigatório, >0)
          - liberado: int (opcional, >=0)
          - observacao: str (opcional, max_length=255)
          - estoque_no_pedido: int (opcional, >=0)
        Retorna a entidade Item_pedido recém-criada.
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

        # valida liberado (se informado)
        liberado = dados.get('liberado')
        if liberado is not None:
            if not isinstance(liberado, int) or liberado < 0:
                raise ValueError("Se fornecido, 'liberado' deve ser um inteiro >= 0.")

        # valida observacao
        observacao = dados.get('observacao', '')
        if not isinstance(observacao, str):
            raise ValueError("'observacao' deve ser uma string.")
        observacao = observacao.strip()[:255]

        # valida estoque_no_pedido (se informado)
        estoque_no_pedido = dados.get('estoque_no_pedido')
        if estoque_no_pedido is not None:
            if not isinstance(estoque_no_pedido, int) or estoque_no_pedido < 0:
                raise ValueError("Se fornecido, 'estoque_no_pedido' deve ser um inteiro >= 0.")

        # monta a entidade de domínio
        item = Item_pedido(
            pedido_id=pedido_id,
            produto_id=produto_id,
            quantidade=quantidade,
            liberado=liberado,
            observacao=observacao,
            estoque_no_pedido=estoque_no_pedido
        )

        # persiste e retorna
        return self.repo.save(item)
