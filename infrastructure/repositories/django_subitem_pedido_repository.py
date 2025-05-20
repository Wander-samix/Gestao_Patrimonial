from typing import List, Optional
from core.domain.entities.subitem_pedido import Subitem_pedido
from core.domain.repositories.subitem_pedido_repository import ISubitem_pedidoRepository
from core.models import SubItemPedido as SubItemPedidoModel

class DjangoSubitem_pedidoRepository(ISubitem_pedidoRepository):
    def save(self, obj: Subitem_pedido) -> Subitem_pedido:
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
        return Subitem_pedido(
            id=m.id,
            pedido_id=m.pedido_id,
            produto_id=m.produto_id,
            quantidade=m.quantidade,
            estoque_no_pedido=m.estoque_no_pedido
        )

    def find_by_id(self, id: int) -> Optional[Subitem_pedido]:
        """
        Busca Subitem_pedido por PK; retorna None se não existir.
        """
        try:
            m = SubItemPedidoModel.objects.get(pk=id)
            return Subitem_pedido(
                id=m.id,
                pedido_id=m.pedido_id,
                produto_id=m.produto_id,
                quantidade=m.quantidade,
                estoque_no_pedido=m.estoque_no_pedido
            )
        except SubItemPedidoModel.DoesNotExist:
            return None

    def list_all(self) -> List[Subitem_pedido]:
        """
        Retorna todos os Subitem_pedido como entidades de domínio.
        """
        return [
            Subitem_pedido(
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
