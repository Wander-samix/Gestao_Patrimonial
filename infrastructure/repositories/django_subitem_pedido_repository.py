from typing import List, Optional
from core.domain.entities.subitem_pedido import SubItemPedido
from core.domain.repositories.subitem_pedido_repository import ISubItemPedidoRepository
from core.models import SubItemPedido as SubItemPedidoModel

class DjangoSubItemPedidoRepository(ISubItemPedidoRepository):
    def save(self, obj: SubItemPedido) -> SubItemPedido:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        """
        if getattr(obj, 'id', None):
            m = SubItemPedidoModel.objects.get(pk=obj.id)
            m.pedido_id         = obj.pedido_id
            m.produto_id        = obj.produto_id
            m.quantidade        = obj.quantidade
            m.estoque_no_pedido = obj.estoque_no_pedido
            m.save(update_fields=['pedido', 'produto', 'quantidade', 'estoque_no_pedido'])
        else:
            m = SubItemPedidoModel.objects.create(
                pedido_id         = obj.pedido_id,
                produto_id        = obj.produto_id,
                quantidade        = obj.quantidade,
                estoque_no_pedido = obj.estoque_no_pedido
            )
        return SubItemPedido(
            id=m.id,
            pedido_id=m.pedido_id,
            produto_id=m.produto_id,
            quantidade=m.quantidade,
            estoque_no_pedido=m.estoque_no_pedido
        )

    def find_by_id(self, id: int) -> Optional[SubItemPedido]:
        """
        Busca SubItemPedido por PK; retorna None se não existir.
        """
        try:
            m = SubItemPedidoModel.objects.get(pk=id)
            return SubItemPedido(
                id=m.id,
                pedido_id=m.pedido_id,
                produto_id=m.produto_id,
                quantidade=m.quantidade,
                estoque_no_pedido=m.estoque_no_pedido
            )
        except SubItemPedidoModel.DoesNotExist:
            return None

    def list_all(self) -> List[SubItemPedido]:
        """
        Retorna todos os SubItemPedido como entidades de domínio.
        """
        return [
            SubItemPedido(
                id=m.id,
                pedido_id=m.pedido_id,
                produto_id=m.produto_id,
                quantidade=m.quantidade,
                estoque_no_pedido=m.estoque_no_pedido
            )
            for m in SubItemPedidoModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove o Subitem_pedido com a PK informada.
        """
        SubItemPedidoModel.objects.filter(pk=id).delete()
