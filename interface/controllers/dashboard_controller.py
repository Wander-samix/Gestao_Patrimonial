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


def dashboard(request):
    # 1) Pega o parâmetro 'data' (YYYY‑MM‑DD). Se inválido ou ausente, usa hoje.
    data_str = request.GET.get('data')
    if data_str:
        try:
            data_mov = datetime.strptime(data_str, '%Y-%m-%d').date()
        except ValueError:
            data_mov = date.today()
    else:
        data_mov = date.today()

    # 2) Contagens básicas
    produtos_count = Produto.objects.count()
    pedidos_count  = Pedido.objects.count()
    usuarios_count = Usuario.objects.count()

    # 3) Pedidos por status
    pedidos_por_status = {
        status: Pedido.objects.filter(status=status).count()
        for status, _ in Pedido.STATUS_CHOICES
    }

    # 4) Entradas totais (quantidade inicial cadastrada)
    entradas_totais = Produto.objects.aggregate(
        total=Sum('quantidade_inicial')
    )['total'] or 0

    # 5) Em Estoque (estoque real): soma de estoque_info.real por combo código+área
    estoque_real_total = 0
    combos = Produto.objects.values('codigo_barras', 'area_id').distinct()
    for combo in combos:
        p = Produto.objects.filter(
            codigo_barras=combo['codigo_barras'],
            area_id=combo['area_id']
        ).first()
        if p:
            estoque_real_total += p.estoque_info(data_limite=data_mov)['real']

    # 6) Valor total em estoque (quantidade * preço_unitário)
    valor_total = Produto.objects.aggregate(
        valor=Sum(
            F('quantidade') * F('preco_unitario'),
            output_field=DecimalField(max_digits=20, decimal_places=2)
        )
    )['valor'] or 0

    # 7) Movimentações e logs do dia
    movimentacoes_dia = (
        MovimentacaoEstoque.objects
        .select_related('produto', 'usuario')
        .filter(data__date=data_mov)
        .order_by('-data')
    )
    logs_dia = LogAcao.objects.filter(data_hora__date=data_mov).order_by('-data_hora')

    return render(request, 'core/dashboard.html', {
        'produtos_count':       produtos_count,
        'pedidos_count':        pedidos_count,
        'usuarios_count':       usuarios_count,
        'pedidos_por_status':   pedidos_por_status,
        'entradas_totais':      entradas_totais,
        'estoque_real_total':   estoque_real_total,
        'valor_total':          valor_total,
        'movimentacoes_dia':    movimentacoes_dia,
        'logs_dia':             logs_dia,
        'data_mov':             data_mov,
        'STATUS_CHOICES':       Pedido.STATUS_CHOICES,
    })

    
# ---------- Importação NFe ----------

@login_required

def exportar_dashboard_excel(request):
    """
    Exporta TODAS as movimentações de estoque como CSV.
    """
    # pega todas as movimentações, em ordem cronológica decrescente
    movimentacoes = (
        MovimentacaoEstoque.objects
        .select_related('produto', 'usuario')
        .order_by('-data')
    )

    # prepara resposta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="movimentacoes_estoque.csv"'

    writer = csv.writer(response)
    # cabeçalho
    writer.writerow(['Tipo', 'Produto', 'Quantidade', 'Usuário', 'Data/Hora'])

    # escreve cada movimentação
    for m in movimentacoes:
        writer.writerow([
            m.get_tipo_display(),
            m.produto.descricao,
            m.quantidade,
            m.usuario.username,
            m.data.strftime('%d/%m/%Y %H:%M'),
        ])

    return response

@login_required

