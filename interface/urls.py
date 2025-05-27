# interface/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers

# — Web (HTML) views —
from interface.controllers.login_controller        import login_view, logout_view
from interface.controllers.produto_controller      import (
    lista_produtos,
    novo_produto,
    editar_produto,
    excluir_produto,
    exportar_produtos_excel,
    bulk_delete_produtos,
    salvar_produto_inline,
    cadastro_produtos,
)
from interface.controllers.nfe_controller          import (
    lista_nfes,
    nova_nfe,
    editar_nfe,
    excluir_nfe,
    upload_nfe,
)
from interface.controllers.fornecedor_controller   import (
    lista_fornecedores,
    novo_fornecedor,
    editar_fornecedor,
    excluir_fornecedor,
)
from interface.controllers.cliente_controller      import (
    lista_clientes,
    novo_cliente,
    editar_cliente,
    excluir_cliente,
)
from interface.controllers.pedido_controller       import (
    lista_pedidos,
    novo_pedido,
    editar_pedido,
    excluir_pedido,
)
from interface.controllers.item_pedido_controller  import (
    lista_item_pedidos,
    novo_item_pedido,
    editar_item_pedido,
    excluir_item_pedido,
)
from interface.controllers.movimentacao_estoque_controller import (
    lista_movimentacoes_estoque,
    nova_movimentacao_estoque,
    editar_movimentacao_estoque,
    excluir_movimentacao_estoque,
)
from interface.controllers.configuracao_controller import (
    configuracoes_view,
    editar_configuracao,
    deletar_configuracao,
)
from interface.controllers.area_controller         import (
    lista_areas,
    nova_area,
    editar_area,
    excluir_area,
)
from interface.controllers.log_acao_controller     import (
    lista_logs_acao,
    novo_log_acao,
    editar_log_acao,
    excluir_log_acao,
)
from interface.controllers.usuario_controller      import (
    lista_usuarios,
    novo_usuario,
    editar_usuario,
    excluir_usuario,
)

# — DRF (API) ViewSets —
from interface.controllers.produto_controller_api              import ProdutoViewSet
from interface.controllers.fornecedor_controller_api           import FornecedorViewSet
from interface.controllers.cliente_controller_api              import ClienteViewSet
from interface.controllers.pedido_controller_api               import PedidoViewSet
from interface.controllers.item_pedido_controller_api          import ItemPedidoViewSet
from interface.controllers.movimentacao_estoque_controller_api import MovimentacaoEstoqueViewSet
from interface.controllers.nfe_controller_api                  import NFeViewSet
from interface.controllers.configuracao_estoque_controller_api import ConfiguracaoEstoqueViewSet
from interface.controllers.area_controller_api                 import AreaViewSet
from interface.controllers.log_acao_controller_api             import LogAcaoViewSet
from interface.controllers.usuario_controller_api              import UsuarioViewSet

# Configura o router do DRF para as rotas de API
router = routers.DefaultRouter()
router.register(r'produtos',              ProdutoViewSet)
router.register(r'fornecedores',          FornecedorViewSet)
router.register(r'clientes',              ClienteViewSet)
router.register(r'pedidos',               PedidoViewSet)
router.register(r'item-pedidos',          ItemPedidoViewSet)
router.register(r'movimentacoes-estoque', MovimentacaoEstoqueViewSet)
router.register(r'nfes',                  NFeViewSet)
router.register(r'configuracoes-estoque', ConfiguracaoEstoqueViewSet)
router.register(r'areas',                 AreaViewSet)
router.register(r'logs-acao',             LogAcaoViewSet)
router.register(r'usuarios',              UsuarioViewSet)

urlpatterns = [
    # — Autenticação —
    path('login/',  login_view,  name='login'),
    path('logout/', logout_view, name='logout'),

    # — Recuperação de senha —
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='core/password_reset_form.html'),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'),
        name='password_reset_complete'
    ),

    # — Dashboard —
    path('dashboard/', lista_produtos, name='dashboard'),

    # — Produtos CRUD e funcionalidades extra —
    path('produtos/',                   lista_produtos,            name='lista_produtos'),
    path('produtos/novo/',              novo_produto,              name='novo_produto'),
    path('produtos/editar/<int:id>/',   editar_produto,            name='editar_produto'),
    path('produtos/excluir/<int:id>/',  excluir_produto,           name='deletar_produto'),
    path('produtos/exportar/',          exportar_produtos_excel,   name='exportar_produtos_excel'),
    path('produtos/upload_nfe/',        upload_nfe,                name='upload_nfe'),
    path('produtos/bulk-delete/',       bulk_delete_produtos,      name='bulk_delete_produtos'),
    path('produtos/salvar-inline/',     salvar_produto_inline,     name='salvar_produto_inline'),

    # — Importação em massa via NFe —
    path('produtos/cadastro-massa/',    cadastro_produtos,         name='cadastro_produtos'),

    # — NFEs CRUD —
    path('nfes/',         lista_nfes,  name='lista_nfes'),
    path('nfes/novo/',    nova_nfe,    name='nova_nfe'),
    path('nfes/editar/<int:id>/',  editar_nfe,   name='editar_nfe'),
    path('nfes/excluir/<int:id>/', excluir_nfe,  name='excluir_nfe'),

    # — Fornecedores —
    path('fornecedores/',           lista_fornecedores,   name='lista_fornecedores'),
    path('fornecedores/novo/',      novo_fornecedor,      name='novo_fornecedor'),
    path('fornecedores/editar/<int:id>/', editar_fornecedor,  name='editar_fornecedor'),
    path('fornecedores/excluir/<int:id>/', excluir_fornecedor, name='excluir_fornecedor'),

    # — Clientes —
    path('clientes/',           lista_clientes,   name='lista_clientes'),
    path('clientes/novo/',      novo_cliente,     name='novo_cliente'),
    path('clientes/editar/<int:id>/', editar_cliente,   name='editar_cliente'),
    path('clientes/excluir/<int:id>/', excluir_cliente, name='excluir_cliente'),

    # — Pedidos —
    path('pedidos/',           lista_pedidos,   name='lista_pedidos'),
    path('pedidos/novo/',      novo_pedido,     name='novo_pedido'),
    path('pedidos/editar/<int:id>/', editar_pedido,   name='editar_pedido'),
    path('pedidos/excluir/<int:id>/', excluir_pedido, name='excluir_pedido'),

    # — Itens de Pedido —
    path('item-pedidos/',           lista_item_pedidos,      name='lista_item_pedidos'),
    path('item-pedidos/novo/',      novo_item_pedido,        name='novo_item_pedido'),
    path('item-pedidos/editar/<int:id>/', editar_item_pedido,   name='editar_item_pedido'),
    path('item-pedidos/excluir/<int:id>/', excluir_item_pedido, name='excluir_item_pedido'),

    # — Movimentações de Estoque —
    path('movimentacoes-estoque/',        lista_movimentacoes_estoque,   name='lista_movimentacoes_estoque'),
    path('movimentacoes-estoque/novo/',   nova_movimentacao_estoque,     name='nova_movimentacao_estoque'),
    path('movimentacoes-estoque/editar/<int:id>/', editar_movimentacao_estoque,   name='editar_movimentacao_estoque'),
    path('movimentacoes-estoque/excluir/<int:id>/', excluir_movimentacao_estoque, name='excluir_movimentacao_estoque'),

    # — Configurações de Estoque —
    path('configuracoes/',                   configuracoes_view,     name='configuracoes'),
    path('configuracoes/editar/<int:area_id>/', editar_configuracao,   name='editar_configuracao'),
    path('configuracoes/deletar/<int:pk>/',     deletar_configuracao,  name='deletar_configuracao'),

    # — Áreas —
    path('areas/',           lista_areas,   name='lista_areas'),
    path('areas/novo/',      nova_area,     name='nova_area'),
    path('areas/editar/<int:id>/', editar_area,   name='editar_area'),
    path('areas/excluir/<int:id>/', excluir_area, name='excluir_area'),

    # — Logs de Ação —
    path('logs-acao/',        lista_logs_acao,    name='lista_logs_acao'),
    path('logs-acao/novo/',   novo_log_acao,      name='novo_log_acao'),
    path('logs-acao/editar/<int:id>/', editar_log_acao,   name='editar_log_acao'),
    path('logs-acao/excluir/<int:id>/', excluir_log_acao, name='excluir_log_acao'),

    # — Usuários —
    path('usuarios/',        lista_usuarios,    name='lista_usuarios'),
    path('usuarios/novo/',   novo_usuario,      name='novo_usuario'),
    path('usuarios/editar/<int:id>/', editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/<int:id>/', excluir_usuario, name='excluir_usuario'),

    # — API routes (DRF) —
    path('api/',      include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
