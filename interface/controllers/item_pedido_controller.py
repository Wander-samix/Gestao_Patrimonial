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

