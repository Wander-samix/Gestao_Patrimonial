from datetime import datetime
from io import BytesIO

from django.shortcuts    import render, redirect, get_object_or_404
from django.contrib      import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from openpyxl import Workbook

from core.models         import Area, ConfiguracaoEstoque, MovimentacaoEstoque
from ..forms.forms       import AreaForm, ConfiguracaoEstoqueForm


def is_admin(user):
    return user.is_superuser or getattr(user, 'papel', None) == 'admin'


@login_required
def configuracoes_view(request):
    areas          = Area.objects.all()
    configuracoes  = ConfiguracaoEstoque.objects.select_related('area')
    # mapeia estoque mínimo (ou 50% padrão)
    minimo = {c.area_id: c.estoque_minimo for c in configuracoes}
    for a in areas:
        a.minimo = minimo.get(a.id, 50)

    form_area   = AreaForm()
    form_config = ConfiguracaoEstoqueForm(initial={'estoque_minimo': 50})

    if request.method == 'POST':
        if 'nova_area' in request.POST:
            form_area = AreaForm(request.POST)
            if form_area.is_valid():
                form_area.save()
                messages.success(request, "Área adicionada.")
                return redirect('configuracoes')

        elif 'nova_configuracao' in request.POST:
            form_config = ConfiguracaoEstoqueForm(request.POST)
            if form_config.is_valid():
                form_config.save()
                messages.success(request, "Configuração adicionada.")
                return redirect('configuracoes')

    return render(request, 'core/configuracoes.html', {
        'areas': areas,
        'configuracoes': configuracoes,
        'form_area': form_area,
        'form_config': form_config,
    })


@login_required
@user_passes_test(is_admin)
def editar_area(request, area_id):
    area = get_object_or_404(Area, id=area_id)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, "Área atualizada.")
    return redirect('configuracoes')


@login_required
@user_passes_test(is_admin)
def deletar_area(request, area_id):
    a = get_object_or_404(Area, id=area_id)
    a.delete()
    messages.success(request, "Área removida.")
    return redirect('configuracoes')


@login_required
@user_passes_test(is_admin)
def editar_configuracao(request, area_id):
    cfg, _ = ConfiguracaoEstoque.objects.get_or_create(
        area_id=area_id, defaults={'estoque_minimo': 50}
    )
    if request.method == 'POST':
        form = ConfiguracaoEstoqueForm(request.POST, instance=cfg)
        if form.is_valid():
            form.save()
            messages.success(request, "Configuração atualizada.")
    return redirect('configuracoes')


@login_required
@user_passes_test(is_admin)
def deletar_configuracao(request, pk):
    cfg = get_object_or_404(ConfiguracaoEstoque, pk=pk)
    cfg.delete()
    messages.success(request, "Configuração removida.")
    return redirect('configuracoes')


@login_required
@user_passes_test(is_admin)
def exportar_sessoes_excel(request):
    """
    Gera um Excel com o número de sessões (MovimentacaoEstoque)
    agrupadas por mês.
    """
    # 1) Agrupa movimentações por mês e conta quantas há em cada um
    sessoes = (
        MovimentacaoEstoque.objects
            .annotate(mes=TruncMonth('data'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
    )

    # 2) Monta o Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Sessões por Mês"
    ws.append(["Mês", "Total de Sessões"])
    for s in sessoes:
        label_mes = s['mes'].strftime("%Y-%m")
        ws.append([label_mes, s['total']])

    # 3) Prepara a resposta HTTP com o arquivo .xlsx
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    hoje = datetime.now().strftime("%Y%m%d")
    filename = f"sessoes_por_mes_{hoje}.xlsx"
    resp = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp
