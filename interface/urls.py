# interface/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views

# Autenticação
from interface.controllers.login_controller import login_view, logout_view

# Produtos
from interface.controllers.produto_controller import (
    lista_produtos,
    novo_produto,
    novo_produto_individual,
    editar_produto,
    excluir_produto,
    exportar_produtos_excel,
    bulk_delete_produtos,
    salvar_produto_inline,
    cadastro_produtos,
    buscar_nome_produto_view,
)

# NFe
from interface.controllers.nfe_controller import (
    lista_nfes,
    nova_nfe,
    editar_nfe,
    excluir_nfe,
    upload_nfe,
)

# Fornecedores
from interface.controllers.fornecedor_controller import (
    lista_fornecedores,
    novo_fornecedor,
    editar_fornecedor,
    excluir_fornecedor,
    ativar_fornecedor,
    desativar_fornecedor,
    salvar_fornecedor_inline,
)

# Clientes
from interface.controllers.cliente_controller import (
    lista_clientes,
    novo_cliente,
    editar_cliente,
    excluir_cliente,
)

# Pedidos
from interface.controllers.pedido_controller import (
    lista_pedidos,
    novo_pedido,
    detalhes_pedido,
    editar_pedido,
    deletar_pedido,
    exportar_pedidos_excel,
)

# Itens de Pedido
from interface.controllers.item_pedido_controller import (
    lista_item_pedidos,
    novo_item_pedido,
    editar_item_pedido,
    excluir_item_pedido,
)

# Movimentações de Estoque
from interface.controllers.movimentacao_estoque_controller import (
    lista_movimentacoes_estoque,
    nova_movimentacao_estoque,
    editar_movimentacao_estoque,
    excluir_movimentacao_estoque,
)

# Dashboard (export)
from interface.controllers.dashboard_controller import exportar_dashboard_excel
from interface.controllers.dashboard_controller import (dashboard, exportar_estoque_por_area_excel,)
from interface.controllers.configuracao_controller import exportar_sessoes_excel

# Configurações
from interface.controllers.configuracao_controller import (
    configuracoes_view,
    editar_area,
    deletar_area,
    editar_configuracao,
    deletar_configuracao,
)

# Áreas (inclui AJAX produtos_por_area)
from interface.controllers.area_controller import (
    lista_areas,
    nova_area,
    editar_area,
    excluir_area,
    produtos_por_area,
)

# Logs de Ação
from interface.controllers.log_acao_controller import (
    lista_logs_acao,
    novo_log_acao,
    editar_log_acao,
    excluir_log_acao,
)

# Usuários e perfil
from interface.controllers.usuario_controller import (
    lista_usuarios,
    novo_usuario,
    editar_usuario,
    excluir_usuario,
    editar_perfil,
    ativar_usuario,
    desativar_usuario,
    deletar_usuario,
    salvar_usuario_inline,
)

# DRF API
from rest_framework import routers
from interface.controllers.produto_controller_api import ProdutoViewSet
from interface.controllers.fornecedor_controller_api import FornecedorViewSet
from interface.controllers.cliente_controller_api import ClienteViewSet
from interface.controllers.pedido_controller_api import PedidoViewSet
from interface.controllers.item_pedido_controller_api import ItemPedidoViewSet
from interface.controllers.movimentacao_estoque_controller_api import MovimentacaoEstoqueViewSet
from interface.controllers.nfe_controller_api import NFeViewSet
from interface.controllers.area_controller_api import AreaViewSet
from interface.controllers.log_acao_controller_api import LogAcaoViewSet
from interface.controllers.usuario_controller_api import UsuarioViewSet

router = routers.DefaultRouter()
router.register(r'produtos',              ProdutoViewSet)
router.register(r'fornecedores',          FornecedorViewSet)
router.register(r'clientes',              ClienteViewSet)
router.register(r'pedidos',               PedidoViewSet)
router.register(r'item-pedidos',          ItemPedidoViewSet)
router.register(r'movimentacoes-estoque', MovimentacaoEstoqueViewSet)
router.register(r'nfes',                  NFeViewSet)
router.register(r'areas',                 AreaViewSet)
router.register(r'logs-acao',             LogAcaoViewSet)
router.register(r'usuarios',              UsuarioViewSet)


urlpatterns = [
    # Home e autenticação
    path('',               login_view,  name='home'),
    path('login/',         login_view,  name='login'),
    path('logout/',        logout_view, name='logout'),

    # Reset de senha
    path('password-reset/',      auth_views.PasswordResetView.as_view(template_name='core/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/',           auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/exportar/', exportar_dashboard_excel, name='exportar_dashboard_excel'),
    path(
        'dashboard/exportar-estoque-por-area/',
        exportar_estoque_por_area_excel,
        name='exportar_estoque_por_area_excel'),

    # Produtos
    path('produtos/',                lista_produtos,          name='lista_produtos'),
    path('produtos/novo/',           novo_produto,            name='novo_produto'),
    path('produtos/novo/individual/',          novo_produto_individual,             name='novo_produto_individual'),
    path('produtos/editar/<int:id>/',editar_produto,          name='editar_produto'),
    path('produtos/excluir/<int:produto_id>/', excluir_produto, name='deletar_produto'),
    path('produtos/exportar/',       exportar_produtos_excel, name='exportar_produtos_excel'),
    path('produtos/bulk-delete/',    bulk_delete_produtos,    name='bulk_delete_produtos'),
    path('produtos/salvar-inline/',  salvar_produto_inline,   name='salvar_produto_inline'),
    path('produtos/upload-nfe/',     upload_nfe,              name='upload_nfe'),
    path('produtos/cadastro-massa/', cadastro_produtos,      name='cadastro_produtos'),

    # NFEs
    path('nfes/',               lista_nfes,   name='lista_nfes'),
    path('nfes/novo/',          nova_nfe,     name='nova_nfe'),
    path('nfes/editar/<int:id>/', editar_nfe, name='editar_nfe'),
    path('nfes/excluir/<int:id>/',excluir_nfe,name='excluir_nfe'),

    # Fornecedores
    path(
        'fornecedores/',
        lista_fornecedores,
        name='lista_fornecedores'
    ),
    path(
        'fornecedores/',
        lista_fornecedores,
        name='fornecedores'
    ),
    path('fornecedores/novo/',             novo_fornecedor,          name='novo_fornecedor'),
    path('fornecedores/ativar/<int:pk>/',  ativar_fornecedor,        name='ativar_fornecedor'),
    path('fornecedores/desativar/<int:pk>/',desativar_fornecedor,     name='desativar_fornecedor'),
    path('fornecedores/editar/<int:id>/',  editar_fornecedor,        name='editar_fornecedor'),
    path('fornecedores/excluir/<int:id>/', excluir_fornecedor,       name='deletar_fornecedor'),
    path('fornecedores/salvar-inline/',    salvar_fornecedor_inline, name='salvar_fornecedor_inline'),

    # Clientes
    path('clientes/',              lista_clientes,  name='lista_clientes'),
    path('clientes/novo/',         novo_cliente,    name='novo_cliente'),
    path('clientes/editar/<int:id>/', editar_cliente,name='editar_cliente'),
    path('clientes/excluir/<int:id>/', excluir_cliente,name='excluir_cliente'),

    # Pedidos
    path('pedidos/',                    lista_pedidos,           name='lista_pedidos'),
    path('pedidos/novo/',               novo_pedido,             name='novo_pedido'),
    path('pedidos/<int:pedido_id>/',    detalhes_pedido,         name='detalhe_pedido'),
    path('pedidos/editar/<int:pedido_id>/', editar_pedido,      name='editar_pedido'),
    path('pedidos/deletar/<int:pedido_id>/', deletar_pedido,   name='deletar_pedido'),
    path('pedidos/exportar/',           exportar_pedidos_excel, name='exportar_pedidos_excel'),

    # Itens de Pedido
    path('item-pedidos/',             lista_item_pedidos,      name='lista_item_pedidos'),
    path('item-pedidos/novo/',        novo_item_pedido,        name='novo_item_pedido'),
    path('item-pedidos/editar/<int:id>/', editar_item_pedido,name='editar_item_pedido'),
    path('item-pedidos/excluir/<int:id>/', excluir_item_pedido,name='excluir_item_pedido'),

    # Movimentações de Estoque
    path('movimentacoes-estoque/',       lista_movimentacoes_estoque,     name='lista_movimentacoes_estoque'),
    path('movimentacoes-estoque/novo/',  nova_movimentacao_estoque,       name='nova_movimentacao_estoque'),
    path('movimentacoes-estoque/editar/<int:id>/', editar_movimentacao_estoque,name='editar_movimentacao_estoque'),
    path('movimentacoes-estoque/excluir/<int:id>/', excluir_movimentacao_estoque,name='excluir_movimentacao_estoque'),

    # Configurações
    path('configuracoes/',                              configuracoes_view,     name='configuracoes'),
    path('configuracoes/editar-area/<int:area_id>/',    editar_area,           name='editar_area'),
    path('configuracoes/deletar-area/<int:area_id>/',   deletar_area,          name='deletar_area'),
    path('configuracoes/editar-configuracao/<int:area_id>/', editar_configuracao, name='editar_configuracao'),
    path('configuracoes/deletar-configuracao/<int:pk>/',     deletar_configuracao,name='deletar_configuracao'),
    path(
        'configuracoes/exportar-sessoes-excel/',
        exportar_sessoes_excel,
        name='exportar_sessoes_excel'
    ),


    # Áreas
    path('areas/',                    lista_areas,      name='lista_areas'),
    path('areas/novo/',               nova_area,        name='nova_area'),
    path('areas/editar/<int:id>/',    editar_area,      name='editar_area'),
    path('areas/excluir/<int:id>/',   excluir_area,     name='excluir_area'),
    path('produtos/por-area/<int:area_id>/', produtos_por_area, name='produtos_por_area'),

    # Logs de Ação
    path('logs-acao/',                lista_logs_acao,    name='lista_logs_acao'),
    path('logs-acao/novo/',           novo_log_acao,      name='novo_log_acao'),
    path('logs-acao/editar/<int:id>/', editar_log_acao,   name='editar_log_acao'),
    path('logs-acao/excluir/<int:id>/', excluir_log_acao, name='excluir_log_acao'),

    # Usuários e perfil
    path('usuarios/',    lista_usuarios,   name='lista_usuarios'),
    path('usuarios/',    lista_usuarios,   name='usuarios'),                # << alias para o template
    path('usuarios/novo/',            novo_usuario,     name='novo_usuario'),
    path('usuarios/ativar/<int:id>/',   ativar_usuario,   name='ativar_usuario'),
    path('usuarios/desativar/<int:id>/',desativar_usuario,name='desativar_usuario'),
    path('usuarios/editar/<int:id>/',   editar_usuario,   name='editar_usuario'),
    path('usuarios/excluir/<int:id>/',  excluir_usuario,  name='excluir_usuario'),
    path('perfil/editar/',              editar_perfil,    name='editar_perfil'),
    path('usuarios/deletar/<int:id>/',  excluir_usuario,  name='deletar_usuario'),
    path('usuarios/salvar-inline/', salvar_usuario_inline, name='salvar_usuario_inline'),

    # DRF API
    path('api/',      include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    #API Cosmos - busca endereço
    path(
      'api/produto/cosmos/<str:codigo>/',
      buscar_nome_produto_view,
      name='buscar_nome_produto')
]
