from typing import List, Optional
from core.domain.entities.saida_produto_por_pedido import Saida_produto_por_pedido
from core.domain.repositories.saida_produto_por_pedido_repository import ISaida_produto_por_pedidoRepository
from core.models import SaidaProdutoPorPedido as SaidaProdutoPorPedidoModel

class DjangoSaida_produto_por_pedidoRepository(ISaida_produto_por_pedidoRepository):
    def save(self, obj: Saida_produto_por_pedido) -> Saida_produto_por_pedido:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Retorna a entidade de domínio com o id gerado/atualizado.
        """
        if getattr(obj, 'id', None):
            m = SaidaProdutoPorPedidoModel.objects.get(pk=obj.id)
            m.produto_id = obj.produto_id
            m.pedido_id  = obj.pedido_id
            m.quantidade = obj.quantidade
            # data_saida é auto_now_add; não alteramos aqui
            m.save(update_fields=['produto', 'pedido', 'quantidade'])
        else:
            m = SaidaProdutoPorPedidoModel.objects.create(
                produto_id=obj.produto_id,
                pedido_id=obj.pedido_id,
                quantidade=obj.quantidade
            )
        return Saida_produto_por_pedido(
            id=m.id,
            produto_id=m.produto_id,
            pedido_id=m.pedido_id,
            quantidade=m.quantidade,
            data_saida=m.data_saida
        )

    def find_by_id(self, id: int) -> Optional[Saida_produto_por_pedido]:
        """
        Busca Saida_produto_por_pedido por PK; retorna None se não existir.
        """
        try:
            m = SaidaProdutoPorPedidoModel.objects.get(pk=id)
            return Saida_produto_por_pedido(
                id=m.id,
                produto_id=m.produto_id,
                pedido_id=m.pedido_id,
                quantidade=m.quantidade,
                data_saida=m.data_saida
            )
        except SaidaProdutoPorPedidoModel.DoesNotExist:
            return None

    def list_all(self) -> List[Saida_produto_por_pedido]:
        """
        Retorna todas as Saidas de produto por pedido como entidades de domínio.
        """
        return [
            Saida_produto_por_pedido(
                id=m.id,
                produto_id=m.produto_id,
                pedido_id=m.pedido_id,
                quantidade=m.quantidade,
                data_saida=m.data_saida
            )
            for m in SaidaProdutoPorPedidoModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove a Saida_produto_por_pedido com a PK informada.
        """
        SaidaProdutoPorPedidoModel.objects.filter(pk=id).delete()
