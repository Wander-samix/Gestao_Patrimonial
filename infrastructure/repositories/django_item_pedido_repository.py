# infrastructure/repositories/django_item_pedido_repository.py

from typing import List, Optional
from core.domain.entities.item_pedido import ItemPedido
from core.domain.repositories.item_pedido_repository import IItemPedidoRepository
from core.models import ItemPedido as ItemPedidoModel

class DjangoItemPedidoRepository(IItemPedidoRepository):
    def save(self, obj: ItemPedido) -> ItemPedido:
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
        return ItemPedido(
            id=model.id,
            pedido_id=model.pedido_id,
            produto_id=model.produto_id,
            quantidade=model.quantidade,
            liberado=model.liberado,
            observacao=model.observacao,
            estoque_no_pedido=model.estoque_no_pedido
        )

    def find_by_id(self, id: int) -> Optional[ItemPedido]:
        """
        Busca ItemPedido por PK; retorna None se não existir.
        """
        try:
            m = ItemPedidoModel.objects.get(pk=id)
            return ItemPedido(
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

    def list_all(self) -> List[ItemPedido]:
        """
        Retorna todos os ItemPedido como entidades de domínio.
        """
        return [
            ItemPedido(
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
        Remove o ItemPedido com a PK informada.
        """
        ItemPedidoModel.objects.filter(pk=id).delete()
