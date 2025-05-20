# core/templatetags/estoque_tags.py
from django import template
from core.domain.entities.pending_statuses import pending_statuses

register = template.Library()

@register.simple_tag
def saldo_no_pedido(produto, pedido):
    """
    Exibe o estoque disponível no momento da solicitação,
    subtraindo reservas de *outros* pedidos.
    """
    return produto.estoque_disponivel(
        data_limite=pedido.data_solicitacao,
        exclude_pedido_id=pedido.id
    )