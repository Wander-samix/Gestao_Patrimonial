from typing import List, Optional
from core.domain.entities.item_pedido import Item_pedido
from core.domain.repositories.item_pedido_repository import IItem_pedidoRepository
from core.models import ItemPedido as ItemPedidoModel

class DjangoItem_pedidoRepository(IItem_pedidoRepository):
    def save(self, obj: Item_pedido) -> Item_pedido:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        """
        if getattr(obj, 'id', None):
            model = ItemPedidoModel.objects.get(pk=obj.id)
            model.pedido_id         = obj.pedido_id
            model.produto_id        = obj.produto_id
            model.quantidade        = obj.quantidade
            model.liberado          = obj.liberado
            model.observacao        = obj.observacao
            model.estoque_no_pedido = obj.estoque_no_pedido
            model.save(update_fields=[
                'pedido', 'produto', 'quantidade', 'liberado',
                'observacao', 'estoque_no_pedido'
            ])
        else:
            model = ItemPedidoModel.objects.create(
                pedido_id         = obj.pedido_id,
                produto_id        = obj.produto_id,
                quantidade        = obj.quantidade,
                liberado          = obj.liberado,
                observacao        = obj.observacao,
                estoque_no_pedido = obj.estoque_no_pedido
            )
        return Item_pedido(
            id=model.id,
            pedido_id=model.pedido_id,
            produto_id=model.produto_id,
            quantidade=model.quantidade,
            liberado=model.liberado,
            observacao=model.observacao,
            estoque_no_pedido=model.estoque_no_pedido
        )

    def find_by_id(self, id: int) -> Optional[Item_pedido]:
        """
        Busca Item_pedido por PK; retorna None se não existir.
        """
        try:
            m = ItemPedidoModel.objects.get(pk=id)
            return Item_pedido(
                id=m.id,
                pedido_id=m.pedido_id,
                produto_id=m.produto_id,
                quantidade=m.quantidade,
                liberado=m.liberado,
                observacao=m.observacao,
                estoque_no_pedido=m.estoque_no_pedido
            )
        except ItemPedidoModel.DoesNotExist:
            return None

    def list_all(self) -> List[Item_pedido]:
        """
        Retorna todos os Item_pedido como entidades de domínio.
        """
        return [
            Item_pedido(
                id=m.id,
                pedido_id=m.pedido_id,
                produto_id=m.produto_id,
                quantidade=m.quantidade,
                liberado=m.liberado,
                observacao=m.observacao,
                estoque_no_pedido=m.estoque_no_pedido
            )
            for m in ItemPedidoModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove o Item_pedido com a PK informada.
        """
        ItemPedidoModel.objects.filter(pk=id).delete()
