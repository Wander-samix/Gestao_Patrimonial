# interface/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views

from interface.controllers.login_controller import login_view, logout_view
from interface.controllers.produto_controller import (
    lista_produtos, cadastro_produtos, editar_produto,
    deletar_produto, salvar_produto_inline,
    buscar_nome_produto_view, registrar_movimentacao,
    upload_nfe, exportar_produtos_excel, produtos_por_area,
    bulk_delete_produtos
)
from interface.controllers.fornecedor_controller_api import (
    fornecedores_view, salvar_fornecedor_inline,
    ativar_fornecedor, desativar_fornecedor,
    editar_fornecedor, deletar_fornecedor
)
from interface.controllers.usuario_controller_api import (
    lista_usuarios, salvar_usuario_inline,
    ativar_usuario, desativar_usuario,
    editar_usuario, deletar_usuario,
    editar_perfil
)
from interface.controllers.area_controller_api import (
    lista_areas, editar_area, deletar_area
)
from interface.controllers.pedido_controller_api import (
    lista_pedidos, novo_pedido, detalhe_pedido,
    aprovar_pedido, separar_pedido, registrar_retirada,
    deletar_pedido, exportar_pedidos_excel
)
from interface.controllers.dashboard_controller import (
    dashboard, exportar_dashboard_excel
)
from interface.controllers.configuracao_controller_api import (
    configuracoes_view, editar_configuracao,
    deletar_configuracao
)
from interface.controllers.log_acao_controller_api import (
    lista_logs, exportar_log_excel
)
from interface.controllers.session_log_controller_api import (
    lista_sessoes, exportar_sessoes_excel
)


urlpatterns = [
    # Autenticação
    path('',            login_view, name='login'),
    path('logout/',     logout_view, name='logout'),

    # Produtos
    path('produtos/',               lista_produtos,           name='lista_produtos'),
    path('produtos/cadastro/',      cadastro_produtos,        name='cadastro_produtos'),
    path('produtos/editar/<int:produto_id>/', editar_produto,   name='editar_produto'),
    path('produtos/deletar/<int:produto_id>/', deletar_produto,   name='deletar_produto'),
    path('produtos/inline/',        salvar_produto_inline,    name='salvar_produto_inline'),
    path('buscar-produto/<str:codigo>/', buscar_nome_produto_view, name='buscar_nome_produto'),
    path('produtos/movimentacao/',  registrar_movimentacao,   name='registrar_movimentacao'),
    path('produtos/upload-nfe/',    upload_nfe,               name='upload_nfe'),
    path('produtos/exportar-excel/',exportar_produtos_excel,  name='exportar_produtos_excel'),
    path('ajax/produtos-por-area/<int:area_id>/', produtos_por_area, name='produtos_por_area'),
    path('produtos/bulk-delete/',   bulk_delete_produtos,     name='bulk_delete_produtos'),

    # Fornecedores
    path('fornecedores/',           fornecedores_view,        name='fornecedores'),
    path('fornecedores/inline/',    salvar_fornecedor_inline, name='salvar_fornecedor_inline'),
    path('fornecedores/ativar/<int:pk>/',   ativar_fornecedor,   name='ativar_fornecedor'),
    path('fornecedores/desativar/<int:pk>/', desativar_fornecedor, name='desativar_fornecedor'),
    path('fornecedores/editar/<int:pk>/',   editar_fornecedor,   name='editar_fornecedor'),
    path('fornecedores/deletar/<int:pk>/',  deletar_fornecedor,  name='deletar_fornecedor'),

    # Usuários
    path('usuarios/',               lista_usuarios,           name='lista_usuarios'),
    path('usuarios/inline/',        salvar_usuario_inline,    name='salvar_usuario_inline'),
    path('usuarios/ativar/<int:usuario_id>/',   ativar_usuario,   name='ativar_usuario'),
    path('usuarios/desativar/<int:usuario_id>/', desativar_usuario, name='desativar_usuario'),
    path('usuarios/editar/<int:usuario_id>/',   editar_usuario,   name='editar_usuario'),
    path('usuarios/deletar/<int:usuario_id>/',  deletar_usuario,  name='deletar_usuario'),
    path('perfil/',                 editar_perfil,           name='editar_perfil'),

    # Áreas
    path('areas/',                  lista_areas,             name='lista_areas'),
    path('configuracoes/area/<int:pk>/editar/', editar_area,    name='editar_area'),
    path('configuracoes/area/<int:pk>/deletar/', deletar_area,  name='deletar_area'),

    # Pedidos
    path('pedidos/',                lista_pedidos,           name='lista_pedidos'),
    path('pedidos/novo/',           novo_pedido,             name='novo_pedido'),
    path('pedidos/<int:pedido_id>/', detalhe_pedido,         name='detalhe_pedido'),
    path('pedidos/<int:pedido_id>/aprovar/', aprovar_pedido,   name='aprovar_pedido'),
    path('pedidos/<int:pedido_id>/separar/', separar_pedido,   name='separar_pedido'),
    path('pedidos/<int:pedido_id>/retirar/', registrar_retirada, name='registrar_retirada'),
    path('pedidos/<int:pedido_id>/deletar/', deletar_pedido,    name='deletar_pedido'),
    path('pedidos/exportar/',       exportar_pedidos_excel,  name='exportar_pedidos_excel'),

    # Dashboard / Configurações
    path('dashboard/',              dashboard,                 name='dashboard'),
    path('dashboard/exportar/',     exportar_dashboard_excel,  name='exportar_dashboard_excel'),
    path('configuracoes/',          configuracoes_view,        name='configuracoes'),
    path('configuracoes/estoque/<int:area_id>/editar/', editar_configuracao, name='editar_configuracao'),
    path('configuracoes/estoque/<int:pk>/deletar/', deletar_configuracao, name='deletar_configuracao'),

    # Logs e Sessões
    path('logs/',                   lista_logs,               name='lista_logs'),
    path('exportar-logs/',          exportar_log_excel,       name='exportar_log_excel'),
    path('sessoes/',                lista_sessoes,            name='lista_sessoes'),
    path('sessoes/exportar/',       exportar_sessoes_excel,   name='exportar_sessoes_excel'),

    # Recuperação de Senha
    path(
        'recuperar-senha/',
        auth_views.PasswordResetView.as_view(template_name="core/recuperar_senha.html"),
        name="password_reset"
    ),
    path(
        'recuperar-senha/enviado/',
        auth_views.PasswordResetDoneView.as_view(template_name="core/recuperar_senha_enviado.html"),
        name="password_reset_done"
    ),
    path(
        'recuperar-senha/confirmar/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="core/recuperar_senha_confirmar.html"),
        name="password_reset_confirm"
    ),
    path(
        'recuperar-senha/completo/',
        auth_views.PasswordResetCompleteView.as_view(template_name="core/recuperar_senha_completo.html"),
        name="password_reset_complete"
    ),
]
