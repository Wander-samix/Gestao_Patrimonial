from typing import Dict, Any, Optional
from datetime import date
from core.domain.entities.pedido import Pedido
from core.domain.repositories.pedido_repository import IPedidoRepository
from infrastructure.repositories.django_pedido_repository import DjangoPedidoRepository

class CriarPedidoService:
    def __init__(self, repo: IPedidoRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoPedidoRepository()

    def execute(self, dados: Dict[str, Any]) -> Pedido:
        """
        dados esperados:
          - codigo: str (obrigatório, max_length=20)
          - usuario_id: int (obrigatório, >0)
          - data_necessaria: date (opcional)
          - observacao: str (opcional)
        Retorna a entidade Pedido recém-criado.
        """
        # valida codigo
        codigo = dados.get('codigo')
        if not codigo or not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("O campo 'codigo' é obrigatório e não pode ser vazio.")
        codigo = codigo.strip()[:20]

        # valida usuario_id
        usuario_id = dados.get('usuario_id')
        if not isinstance(usuario_id, int) or usuario_id < 1:
            raise ValueError("O campo 'usuario_id' é obrigatório e deve ser um inteiro positivo.")

        # valida data_necessaria (opcional)
        data_necessaria: Optional[date] = dados.get('data_necessaria')
        if data_necessaria is not None and not isinstance(data_necessaria, date):
            raise ValueError("'data_necessaria' deve ser um objeto date, se informado.")

        # valida observacao (opcional)
        observacao: Optional[str] = dados.get('observacao')
        if observacao is not None:
            if not isinstance(observacao, str):
                raise ValueError("'observacao' deve ser uma string.")
            observacao = observacao.strip()

        # monta a entidade de domínio
        pedido = Pedido(
            codigo=codigo,
            usuario_id=usuario_id,
            data_necessaria=data_necessaria,
            observacao=observacao
        )

        # persiste e retorna
        return self.repo.save(pedido)
