from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.utils import IntegrityError
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.db.models.functions import TruncMonth
from openpyxl import Workbook
from django.db.models import Q, Sum, Max, Min, F, DecimalField

from core.models import (
    Produto, Fornecedor, Usuario, MovimentacaoEstoque,
    Area, Pedido, ItemPedido, LogAcao, ConfiguracaoEstoque
)

from ..forms.forms import AreaForm, ConfiguracaoEstoqueForm

# Define aqui o seu teste de admin
def is_admin(user):
    return user.is_superuser or getattr(user, 'papel', None) == 'admin'


@login_required
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
        if 'nova_area' in request.POST:
            form_area = AreaForm(request.POST)
            if form_area.is_valid():
                form_area.save()
                messages.success(request, "Área adicionada com sucesso.")
                return redirect('configuracoes')

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


@login_required
@user_passes_test(is_admin)
def editar_configuracao(request, area_id):
    cfg, _ = ConfiguracaoEstoque.objects.get_or_create(
        area_id=area_id,
        defaults={'estoque_minimo': 50}
    )
    if request.method == 'POST':
        form = ConfiguracaoEstoqueForm(request.POST, instance=cfg)
        if form.is_valid():
            form.save()
            messages.success(request, "Configuração atualizada com sucesso.")
    return redirect('configuracoes')


@login_required
@user_passes_test(is_admin)
def deletar_configuracao(request, pk):
    cfg = get_object_or_404(ConfiguracaoEstoque, pk=pk)
    cfg.delete()
    messages.success(request, "Configuração removida.")
    return redirect("configuracoes")
