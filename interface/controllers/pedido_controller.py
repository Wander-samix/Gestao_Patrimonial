from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.utils import IntegrityError
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models.functions import TruncMonth
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
import xml.etree.ElementTree as ET
import json
import requests
from openpyxl import Workbook
from django.db.models import Q, Sum, Max, Min, F, DecimalField
from django.views.decorators.http import require_GET
from itertools import zip_longest
from core.models import (
    Produto, Fornecedor, Usuario, MovimentacaoEstoque,
    Area, Pedido, ItemPedido, LogAcao,
    ConfiguracaoEstoque)
from ..forms.forms import AreaForm, ConfiguracaoEstoqueForm
from django.db import transaction
from django import template
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from ..forms.forms import ProfileForm
from ..forms.forms import ProdutoForm
import csv
from datetime import date, datetime
from django.shortcuts import render
from core.models import SessionLog
from django.core.paginator import Paginator
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from django.db.models import OuterRef, Subquery
from core.models import SaidaProdutoPorPedido


register = template.Library()
User = get_user_model()

PENDING_STATUSES = [
    'aguardando_aprovacao',
    'aprovado',
    'separado',
]


def lista_pedidos(request):
    status = request.GET.get("status")
    ordenar_por = request.GET.get("ordenar_por", "-data_solicitacao")  # padrão decrescente
    pagina = request.GET.get("page")

    # Filtra pedidos por papel do usuário
    if request.user.papel in ['admin', 'tecnico']:
        pedidos_qs = Pedido.objects.all()
    else:
        pedidos_qs = Pedido.objects.filter(usuario=request.user)

    # Filtro por status
    if status:
        pedidos_qs = pedidos_qs.filter(status=status)

    # Ordenação (campo pode ser passado com "-" para ordem decrescente)
    pedidos_qs = pedidos_qs.order_by(ordenar_por)

    # Paginação
    paginator = Paginator(pedidos_qs, 10)
    pedidos = paginator.get_page(pagina)

    return render(request, 'core/lista_pedidos.html', {
        'pedidos': pedidos,
        'STATUS_CHOICES': Pedido.STATUS_CHOICES,
        'areas': Area.objects.all(),
        'produtos': Produto.objects.filter(status='ativo'),
        'status_selecionado': status,
        'ordenar_por': ordenar_por.lstrip('-'),
        'ordem': 'desc' if ordenar_por.startswith('-') else 'asc',
    })


@login_required
@transaction.atomic

def novo_pedido(request):
    if request.method == "POST":
        # 1) Código
        ultimo_id = Pedido.objects.aggregate(Max("id"))["id__max"] or 0
        codigo = f"PD{str(ultimo_id + 1).zfill(5)}"

        # 2) Status inicial e quem aprova
        if request.user.papel in ["admin", "tecnico"]:
            status_inicial = "aprovado"
            aprovado_por = request.user
            data_aprovacao = now()
        else:
            status_inicial = "aguardando_aprovacao"
            aprovado_por = None
            data_aprovacao = None

        # 3) Cria o Pedido
        data_necessaria_pedido = request.POST.get('data_necessaria') or None
        pedido = Pedido.objects.create(
            codigo=codigo,
            usuario=request.user,
            status=status_inicial,
            aprovado_por=aprovado_por,
            data_aprovacao=data_aprovacao,
            data_necessaria=data_necessaria_pedido,
        )

        # 4) Laço sobre os itens vindos do form
        hoje = now().date()
        area_ids    = request.POST.getlist('area_id')
        produto_ids = request.POST.getlist('produto_id')
        quantidades = request.POST.getlist('quantidade')
        observacoes = request.POST.getlist('obs_item')

        for area_id, prod_id, qt, obs in zip_longest(area_ids, produto_ids, quantidades, observacoes, fillvalue=''):
            if not (area_id and prod_id and qt):
                continue

            # valida quantidade
            try:
                quantidade = int(qt)
                if quantidade <= 0:
                    raise ValueError()
            except (ValueError, TypeError):
                messages.error(request, f"Quantidade inválida para o produto {prod_id}.")
                continue

            # bloqueio para consistência
            inst = get_object_or_404(
                Produto.objects.select_for_update(),
                pk=int(prod_id)
            )

            # confirma área
            if inst.area_id != int(area_id):
                messages.error(
                    request,
                    f"Produto {inst.descricao} não pertence à área selecionada."
                )
                raise ValueError("Área inconsistente com o produto")

            # usa estoque_info para obter o disponível projetado
            info = inst.estoque_info(data_limite=hoje)
            estoque_disp = info['disponivel']

            if estoque_disp < quantidade:
                messages.error(
                    request,
                    f"Estoque insuficiente para {inst.descricao} na área {inst.area.nome}. "
                    f"Disponível: {estoque_disp}, Solicitado: {quantidade}."
                )
                raise ValueError("Estoque insuficiente")

            # cria o ItemPedido, guardando o estoque no momento
            ItemPedido.objects.create(
                pedido=pedido,
                produto=inst,
                quantidade=quantidade,
                observacao=obs.strip(),
                estoque_no_pedido=estoque_disp
            )

        # 5) Feedback
        if status_inicial == "aprovado":
            messages.success(request, "Pedido aprovado com sucesso!")
        else:
            messages.success(request, "Pedido registrado com sucesso! Aguardando aprovação.")

        return redirect("lista_pedidos")

    # GET: render do form
    if request.user.papel in ['admin', 'tecnico']:
        areas = Area.objects.all()
    else:
        areas = request.user.areas.all()

    return render(request, "core/novo_pedido.html", {
        "areas": areas,
        "areas_json": json.dumps(
            list(areas.values("id", "nome")),
            cls=DjangoJSONEncoder
        ),
    })

@login_required
@transaction.atomic

def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    is_admin = request.user.papel == 'admin'

    # Bloqueia POST para não-admins
    if request.method == 'POST' and not is_admin:
        return redirect('lista_pedidos')

    if request.method == 'POST':
        action = request.POST.get('action')

        # Aprovar pedido → dispara a baixa de estoque em todos os lotes
        if action == 'approve' and pedido.status == 'aguardando_aprovacao':
            pedido.aprovar(request.user)
            messages.success(request, "Pedido aprovado com sucesso! Estoque atualizado.")

        # Reprovar pedido
        elif action == 'reject' and pedido.status == 'aguardando_aprovacao':
            pedido.status = 'rejeitado'
            pedido.save()
            messages.success(request, "Pedido rejeitado.")

        # Separar pedido → só marca a quantidade liberada e muda status
        elif action == 'separar' and pedido.status == 'aprovado':
            for item in pedido.itens.all():
                raw = request.POST.get(f'liberado_{item.id}')
                liberado = int(raw) if raw and raw.isdigit() else 0

                # Limita ao saldo que havia no momento do pedido
                estoque_no_pedido = item.estoque_no_pedido or 0
                item.liberado = min(liberado, item.quantidade, estoque_no_pedido)
                item.save()

            pedido.marcar_como_separado()
            messages.success(request, "Pedido marcado como separado.")

        # Retirar pedido → dispara apenas o log de saída e muda status para entregue
        elif action == 'retirar' and pedido.status == 'separado':
            quem = request.POST.get('retirado_por') or request.user.username
            pedido.registrar_retirada(quem)
            messages.success(request, "Pedido registrado como retirado.")

        else:
            messages.error(request, "Ação não permitida ou estado inválido.")

        return redirect('lista_pedidos')

    # GET: exibe lista de pedidos
    pedidos = Pedido.objects.select_related('usuario').prefetch_related('itens__produto')
    return render(request, 'core/lista_pedidos.html', {
        'pedidos': pedidos,
        'status_selecionado': request.GET.get('status', ''),
        'is_admin': is_admin,
        'STATUS_CHOICES': Pedido.STATUS_CHOICES,
    })

def aprovar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.status != 'aguardando_aprovacao':
        messages.warning(request, "Este pedido já foi aprovado.")
        return redirect('detalhes_pedido', pedido_id=pedido.id)

    for item in pedido.itens.all():
        qtd_restante = item.quantidade
        produtos = Produto.objects.filter(
            codigo_barras=item.produto.codigo_barras,
            area=item.produto.area,
            quantidade__gt=0
        ).order_by('criado_em', 'validade')

        for prod in produtos:
            if qtd_restante == 0:
                break
            if prod.quantidade >= qtd_restante:
                prod.quantidade -= qtd_restante
                prod.save()
                qtd_restante = 0
            else:
                qtd_restante -= prod.quantidade
                prod.quantidade = 0
                prod.save()

        if qtd_restante > 0:
            messages.error(request, f"Estoque insuficiente para o produto {item.produto.descricao}")
            transaction.set_rollback(True)
            return redirect('detalhes_pedido', pedido_id=pedido.id)

        # Atualiza o item.produto para refletir a nova soma
        item.produto.quantidade = Produto.objects.filter(
            codigo_barras=item.produto.codigo_barras,
            area=item.produto.area
        ).aggregate(total=Sum('quantidade'))['total'] or 0
        item.produto.save(update_fields=['quantidade'])

    pedido.aprovar(request.user)
    pedido.data_aprovacao = now()
    pedido.save()

    messages.success(request, "Pedido aprovado com sucesso. Estoque atualizado.")
    return redirect('detalhes_pedido', pedido_id=pedido.id)



@login_required

def separar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.status == 'aprovado':
        pedido.marcar_como_separado()
        if pedido.usuario.email:
            send_mail(
                subject='Pedido separado!',
                message=f'Seu pedido {pedido.codigo} foi separado e está disponível para retirada.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[pedido.usuario.email],
                fail_silently=True
            )
        messages.success(request, f"Pedido {pedido.codigo} marcado como separado.")
    else:
        messages.error(request, "Pedido não está no status correto para separação.")
    return redirect('lista_pedidos')

@login_required

def registrar_retirada(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        nome = request.POST.get('retirado_por')
        if nome:
            pedido.registrar_retirada(nome)
            messages.success(request, f"Pedido {pedido.codigo} registrado como retirado.")
        else:
            messages.error(request, "Informe quem retirou o pedido.")
    return redirect('lista_pedidos')

def deletar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()
    messages.success(request, f"Pedido {pedido.codigo} excluído com sucesso.")
    return redirect('lista_pedidos')


@login_required
@user_passes_test(is_admin)

def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    is_admin = request.user.papel == 'admin'

    # Bloqueia POST para não-admins
    if request.method == 'POST' and not is_admin:
        return redirect('lista_pedidos')

    if request.method == 'POST':
        action = request.POST.get('action')

        # Aprovar pedido → dispara a baixa de estoque em todos os lotes
        if action == 'approve' and pedido.status == 'aguardando_aprovacao':
            pedido.aprovar(request.user)
            messages.success(request, "Pedido aprovado com sucesso! Estoque atualizado.")

        # Reprovar pedido
        elif action == 'reject' and pedido.status == 'aguardando_aprovacao':
            pedido.status = 'rejeitado'
            pedido.save()
            messages.success(request, "Pedido rejeitado.")

        # Separar pedido → só marca a quantidade liberada e muda status
        elif action == 'separar' and pedido.status == 'aprovado':
            for item in pedido.itens.all():
                raw = request.POST.get(f'liberado_{item.id}')
                liberado = int(raw) if raw and raw.isdigit() else 0

                # Limita ao saldo que havia no momento do pedido
                estoque_no_pedido = item.estoque_no_pedido or 0
                item.liberado = min(liberado, item.quantidade, estoque_no_pedido)
                item.save()

            pedido.marcar_como_separado()
            messages.success(request, "Pedido marcado como separado.")

        # Retirar pedido → dispara apenas o log de saída e muda status para entregue
        elif action == 'retirar' and pedido.status == 'separado':
            quem = request.POST.get('retirado_por') or request.user.username
            pedido.registrar_retirada(quem)
            messages.success(request, "Pedido registrado como retirado.")

        else:
            messages.error(request, "Ação não permitida ou estado inválido.")

        return redirect('lista_pedidos')

    # GET: exibe lista de pedidos
    pedidos = Pedido.objects.select_related('usuario').prefetch_related('itens__produto')
    return render(request, 'core/lista_pedidos.html', {
        'pedidos': pedidos,
        'status_selecionado': request.GET.get('status', ''),
        'is_admin': is_admin,
        'STATUS_CHOICES': Pedido.STATUS_CHOICES,
    })

def exportar_pedidos_excel(request):
    pedidos = Pedido.objects.select_related('usuario', 'aprovado_por')\
                            .prefetch_related('itens__produto__area', 'subitens__produto__area')\
                            .order_by('-data_solicitacao')

    wb = Workbook()
    ws = wb.active
    ws.title = "Pedidos"

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="4F81BD")
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)

    headers = [
        "Código", "Data Solicitação", "Solicitante", "Email", "Necessário em", "Status",
        "Aprovado por", "Data Aprovação", "Separado em", "Retirado por", "Data Retirada",
        "Produto", "Código de Barras", "Área", "Qtd Solicitada", "Qtd Liberada", "Estoque Disp.", "Observação"
    ]
    ws.append(headers)

    for col_num, col_name in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_num, value=col_name)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center

    row = 2
    for pedido in pedidos:
        itens = list(pedido.itens.all())
        subitens = list(pedido.subitens.all())
        total_linhas = len(itens) + len(subitens)
        start_row = row

        for item in itens:
            produto = item.produto
            ws.append([
                "", "", "", "", "", "", "", "", "", "", "",
                produto.descricao if produto else "",
                produto.codigo_barras if produto else "",
                produto.area.nome if produto and produto.area else "",
                item.quantidade,
                item.liberado if item.liberado is not None else item.quantidade,
                item.estoque_no_pedido or "",
                item.observacao or ""
            ])
            row += 1

        for subitem in subitens:
            produto = subitem.produto
            ws.append([
                "", "", "", "", "", "", "", "", "", "", "",
                f"{produto.descricao} (subitem)" if produto else "",
                produto.codigo_barras if produto else "",
                produto.area.nome if produto and produto.area else "",
                subitem.quantidade,
                "—",
                subitem.estoque_no_pedido or "",
                ""
            ])
            row += 1

        if total_linhas == 0:
            ws.append([
                pedido.codigo,
                pedido.data_solicitacao.strftime('%d/%m/%Y %H:%M') if pedido.data_solicitacao else "",
                pedido.usuario.username if pedido.usuario else "",
                pedido.usuario.email if pedido.usuario else "",
                pedido.data_necessaria.strftime('%d/%m/%Y') if pedido.data_necessaria else "",
                pedido.get_status_display(),
                pedido.aprovado_por.username if pedido.aprovado_por else "",
                pedido.data_aprovacao.strftime('%d/%m/%Y %H:%M') if pedido.data_aprovacao else "",
                pedido.data_separacao.strftime('%d/%m/%Y %H:%M') if pedido.data_separacao else "",
                pedido.retirado_por or "",
                pedido.data_retirada.strftime('%d/%m/%Y %H:%M') if pedido.data_retirada else "",
            ] + [""] * 7)
            row += 1
        else:
            for col, val in enumerate([
                pedido.codigo,
                pedido.data_solicitacao.strftime('%d/%m/%Y %H:%M') if pedido.data_solicitacao else "",
                pedido.usuario.username if pedido.usuario else "",
                pedido.usuario.email if pedido.usuario else "",
                pedido.data_necessaria.strftime('%d/%m/%Y') if pedido.data_necessaria else "",
                pedido.get_status_display(),
                pedido.aprovado_por.username if pedido.aprovado_por else "",
                pedido.data_aprovacao.strftime('%d/%m/%Y %H:%M') if pedido.data_aprovacao else "",
                pedido.data_separacao.strftime('%d/%m/%Y %H:%M') if pedido.data_separacao else "",
                pedido.retirado_por or "",
                pedido.data_retirada.strftime('%d/%m/%Y %H:%M') if pedido.data_retirada else ""
            ], start=1):
                ws.merge_cells(start_row=start_row, end_row=row-1, start_column=col, end_column=col)
                ws.cell(row=start_row, column=col, value=val).alignment = center

    # Auto ajuste largura
    for col in ws.columns:
        max_length = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = max_length + 2

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename=pedidos.xlsx'
    wb.save(response)
    return response

@login_required
@user_passes_test(is_admin)

