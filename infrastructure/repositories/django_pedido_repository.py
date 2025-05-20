from typing import List, Optional
from core.domain.entities.pedido import Pedido
from core.domain.repositories.pedido_repository import IPedidoRepository
from core.models import Pedido as PedidoModel

class DjangoPedidoRepository(IPedidoRepository):
    def save(self, obj: Pedido) -> Pedido:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Retorna a entidade de domínio com o id gerado/atualizado.
        """
        if getattr(obj, 'id', None):
            m = PedidoModel.objects.get(pk=obj.id)
            m.codigo           = obj.codigo
            m.usuario_id       = obj.usuario_id
            m.status           = obj.status
            m.aprovado_por_id  = obj.aprovado_por_id
            m.data_aprovacao   = obj.data_aprovacao
            m.data_separacao   = obj.data_separacao
            m.data_retirada    = obj.data_retirada
            m.retirado_por     = obj.retirado_por
            m.observacao       = obj.observacao
            m.data_necessaria  = obj.data_necessaria
            m.save(update_fields=[
                'codigo', 'usuario', 'status', 'aprovado_por',
                'data_aprovacao', 'data_separacao', 'data_retirada',
                'retirado_por', 'observacao', 'data_necessaria'
            ])
        else:
            m = PedidoModel.objects.create(
                codigo          = obj.codigo,
                usuario_id      = obj.usuario_id,
                data_necessaria = obj.data_necessaria,
                observacao      = obj.observacao
            )
        return Pedido(
            id=m.id,
            codigo=m.codigo,
            usuario_id=m.usuario_id,
            data_solicitacao=m.data_solicitacao,
            status=m.status,
            aprovado_por_id=m.aprovado_por_id,
            data_aprovacao=m.data_aprovacao,
            data_separacao=m.data_separacao,
            data_retirada=m.data_retirada,
            retirado_por=m.retirado_por,
            observacao=m.observacao,
            data_necessaria=m.data_necessaria
        )

    def find_by_id(self, id: int) -> Optional[Pedido]:
        """
        Busca Pedido por PK; retorna None se não existir.
        """
        try:
            m = PedidoModel.objects.get(pk=id)
            return Pedido(
                id=m.id,
                codigo=m.codigo,
                usuario_id=m.usuario_id,
                data_solicitacao=m.data_solicitacao,
                status=m.status,
                aprovado_por_id=m.aprovado_por_id,
                data_aprovacao=m.data_aprovacao,
                data_separacao=m.data_separacao,
                data_retirada=m.data_retirada,
                retirado_por=m.retirado_por,
                observacao=m.observacao,
                data_necessaria=m.data_necessaria
            )
        except PedidoModel.DoesNotExist:
            return None

    def list_all(self) -> List[Pedido]:
        """
        Retorna todos os Pedidos como entidades de domínio.
        """
        return [
            Pedido(
                id=m.id,
                codigo=m.codigo,
                usuario_id=m.usuario_id,
                data_solicitacao=m.data_solicitacao,
                status=m.status,
                aprovado_por_id=m.aprovado_por_id,
                data_aprovacao=m.data_aprovacao,
                data_separacao=m.data_separacao,
                data_retirada=m.data_retirada,
                retirado_por=m.retirado_por,
                observacao=m.observacao,
                data_necessaria=m.data_necessaria
            )
            for m in PedidoModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove o Pedido com a PK informada.
        """
        PedidoModel.objects.filter(pk=id).delete()
