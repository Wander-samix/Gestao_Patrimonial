# core/templatetags/saldo.py
from django import template
register = template.Library()

@register.filter
def saldo_para(produto, data_limite):
    return produto.estoque_disponivel(data_limite)
