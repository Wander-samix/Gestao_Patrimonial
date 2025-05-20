from typing import Dict, Any
from core.domain.entities.saida_produto_por_pedido import Saida_produto_por_pedido
from core.domain.repositories.saida_produto_por_pedido_repository import ISaida_produto_por_pedidoRepository
from infrastructure.repositories.django_saida_produto_por_pedido_repository import DjangoSaida_produto_por_pedidoRepository

class CriarSaida_produto_por_pedidoService:
    def __init__(self, repo: ISaida_produto_por_pedidoRepository = None):
        # Injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoSaida_produto_por_pedidoRepository()

    def execute(self, dados: Dict[str, Any]) -> Saida_produto_por_pedido:
        """
        dados esperados:
          - produto_id: int (obrigatório, >0)
          - pedido_id: int (obrigatório, >0)
          - quantidade: int (obrigatório, >0)
        Retorna a entidade Saida_produto_por_pedido recém-criada.
        """
        # valida produto_id
        produto_id = dados.get('produto_id')
        if not isinstance(produto_id, int) or produto_id < 1:
            raise ValueError("O campo 'produto_id' é obrigatório e deve ser um inteiro positivo.")

        # valida pedido_id
        pedido_id = dados.get('pedido_id')
        if not isinstance(pedido_id, int) or pedido_id < 1:
            raise ValueError("O campo 'pedido_id' é obrigatório e deve ser um inteiro positivo.")

        # valida quantidade
        quantidade = dados.get('quantidade')
        if not isinstance(quantidade, int) or quantidade < 1:
            raise ValueError("O campo 'quantidade' é obrigatório e deve ser um inteiro maior que zero.")

        # monta a entidade de domínio
        saida = Saida_produto_por_pedido(
            produto_id=produto_id,
            pedido_id=pedido_id,
            quantidade=quantidade
        )

        # persiste e retorna
        return self.repo.save(saida)
