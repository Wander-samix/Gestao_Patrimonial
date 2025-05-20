# interface/urls.py
from django.urls import path

from interface.controllers.area_controller import criar_area
from interface.controllers.cliente_controller import criar_cliente
from interface.controllers.configuracao_estoque_controller import criar_configuracao_estoque
from interface.controllers.fornecedor_controller import criar_fornecedor
from interface.controllers.item_pedido_controller import criar_item_pedido
from interface.controllers.log_acao_controller import criar_log_acao
from interface.controllers.movimentacao_estoque_controller import criar_movimentacao_estoque
from interface.controllers.nfe_controller import criar_nfe
from interface.controllers.pedido_controller import criar_pedido
from interface.controllers.produto_controller import criar_produto
from interface.controllers.saida_produto_por_pedido_controller import criar_saida_produto_por_pedido
from interface.controllers.session_log_controller import criar_session_log
from interface.controllers.subitem_pedido_controller import criar_subitem_pedido
from interface.controllers.usuario_controller import criar_usuario

urlpatterns = [
    path('areas/', criar_area, name='api_criar_area'),
    path('clientes/', criar_cliente, name='api_criar_cliente'),
    path('configuracoes-estoque/', criar_configuracao_estoque, name='api_criar_configuracao_estoque'),
    path('fornecedores/', criar_fornecedor, name='api_criar_fornecedor'),
    path('item-pedidos/', criar_item_pedido, name='api_criar_item_pedido'),
    path('logs-acoes/', criar_log_acao, name='api_criar_log_acao'),
    path('movimentacoes-estoque/', criar_movimentacao_estoque, name='api_criar_movimentacao_estoque'),
    path('nfes/', criar_nfe, name='api_criar_nfe'),
    path('pedidos/', criar_pedido, name='api_criar_pedido'),
    path('produtos/', criar_produto, name='api_criar_produto'),
    path('saidas-produto-por-pedido/', criar_saida_produto_por_pedido, name='api_criar_saida_produto_por_pedido'),
    path('session-logs/', criar_session_log, name='api_criar_session_log'),
    path('subitens-pedido/', criar_subitem_pedido, name='api_criar_subitem_pedido'),
    path('usuarios/', criar_usuario, name='api_criar_usuario'),
]
