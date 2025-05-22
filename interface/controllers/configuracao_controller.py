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


def configuracoes_view(request):
    # --- Dados principais ---
    areas = list(Area.objects.all())
    configuracoes = ConfiguracaoEstoque.objects.select_related('area')

    # Mapeia cada área ao seu estoque mínimo; padrão 50%
    minimo_por_area = {
        cfg.area_id: cfg.estoque_minimo
        for cfg in configuracoes if cfg.area_id
    }
    for area in areas:
        area.minimo = minimo_por_area.get(area.id, 50)

    # --- Forms iniciais ---
    form_area = AreaForm()
    form_config = ConfiguracaoEstoqueForm(initial={'estoque_minimo': 50})

    # --- Tratamento de POST ---
    if request.method == 'POST':
        # Adicionar nova área
        if 'nova_area' in request.POST:
            form_area = AreaForm(request.POST)
            if form_area.is_valid():
                form_area.save()
                messages.success(request, "Área adicionada com sucesso.")
                return redirect('configuracoes')
        # Salvar nova configuração de estoque mínimo
        elif 'nova_configuracao' in request.POST:
            form_config = ConfiguracaoEstoqueForm(request.POST)
            if form_config.is_valid():
                form_config.save()
                messages.success(request, "Configuração salva com sucesso.")
                return redirect('configuracoes')

    # --- Renderiza a página de configurações ---
    return render(request, 'core/configuracoes.html', {
        'areas': areas,
        'configuracoes': configuracoes,
        'form_area': form_area,
        'form_config': form_config,
    })

# ---------- Áreas ----------

def editar_configuracao(request, area_id):
    # get_or_create para não falhar quando ainda não existir
    cfg, _ = ConfiguracaoEstoque.objects.get_or_create(
        area_id=area_id,
        defaults={'estoque_minimo': 50}
    )
    if request.method == 'POST':
        form = ConfiguracaoEstoqueForm(request.POST, instance=cfg)
        if form.is_valid():
            form.save()
    return redirect('configuracoes')

@login_required
@user_passes_test(is_admin)

def deletar_configuracao(request, pk):
    cfg = get_object_or_404(ConfiguracaoEstoque, pk=pk)
    cfg.delete()
    messages.success(request, "Configuração removida.")
    return redirect("configuracoes")

