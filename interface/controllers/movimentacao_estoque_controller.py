from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import MovimentacaoEstoque
from django.http                import HttpResponse
import csv


@login_required
def exportar_dashboard_excel(request):
    movimentacoes = MovimentacaoEstoque.objects.select_related('produto', 'usuario')\
                                               .order_by('-data')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="movimentacoes_estoque.csv"'
    writer = csv.writer(response)
    writer.writerow(['Tipo', 'Produto', 'Quantidade', 'Usuário', 'Data/Hora'])
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
def lista_movimentacoes_estoque(request):
    movimentacoes = MovimentacaoEstoque.objects.all()
    return render(request, 'movimentacao_estoque/lista.html', {'movimentacoes_estoque': movimentacoes})


@login_required
def nova_movimentacao_estoque(request):
    if request.method == 'POST':
        data = request.POST.dict()
        MovimentacaoEstoque.objects.create(**data)
        messages.success(request, 'Movimentação de estoque cadastrada com sucesso.')
        return redirect(reverse('lista_movimentacoes_estoque'))
    return render(request, 'movimentacao_estoque/novo.html')


@login_required
def editar_movimentacao_estoque(request, id):
    mov = get_object_or_404(MovimentacaoEstoque, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(mov, key, value)
        mov.save()
        messages.success(request, 'Movimentação de estoque atualizada com sucesso.')
        return redirect(reverse('lista_movimentacoes_estoque'))
    return render(request, 'movimentacao_estoque/editar.html', {'movimentacao_estoque': mov})


@login_required
def excluir_movimentacao_estoque(request, id):
    mov = get_object_or_404(MovimentacaoEstoque, id=id)
    mov.delete()
    messages.success(request, 'Movimentação de estoque excluída com sucesso.')
    return redirect(reverse('lista_movimentacoes_estoque'))
