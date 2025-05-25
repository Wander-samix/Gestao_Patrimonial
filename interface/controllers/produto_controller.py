# interface/controllers/produto_controller.py

import csv
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Produto
from interface.forms.forms import ProdutoForm


@login_required
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'core/lista_produtos.html', {
        'produtos': produtos
    })


@login_required
def novo_produto(request):
    form = ProdutoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Produto cadastrado com sucesso.')
        return redirect(reverse('lista_produtos'))
    return render(request, 'core/cadastro_produtos.html', {
        'form': form
    })


@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    form = ProdutoForm(request.POST or None, instance=produto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Produto atualizado com sucesso.')
        return redirect(reverse('lista_produtos'))
    return render(request, 'core/editar_produto.html', {
        'form': form,
        'produto': produto
    })


@login_required
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    messages.success(request, 'Produto excluído com sucesso.')
    return redirect(reverse('lista_produtos'))


@login_required
def exportar_produtos_excel(request):
    """
    Exporta todos os produtos em CSV para serem abertos no Excel.
    """
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="produtos.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nome', 'Quantidade', 'Preço'])
    for p in Produto.objects.all():
        writer.writerow([p.id, p.nome, p.quantidade, p.preco])
    return response


@login_required
def bulk_delete_produtos(request):
    """
    Recebe JSON {"ids": [1,2,3]} via POST e exclui esses produtos.
    Retorna JSON {sucesso: true} ou {sucesso: false, erro: "..."}.
    """
    if request.method != 'POST':
        return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'}, status=405)

    try:
        payload = json.loads(request.body)
        ids = payload.get('ids', [])
        Produto.objects.filter(id__in=ids).delete()
        return JsonResponse({'sucesso': True})
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)})

@login_required
def salvar_produto_inline(request):
    """
    Recebe JSON com os campos de um produto, cadastra e devolve {sucesso: true}.
    """
    if request.method != 'POST':
        return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'}, status=405)

    try:
        dados = json.loads(request.body)
        # Se preferir usar o form:
        form = ProdutoForm(dados)
        if not form.is_valid():
            return JsonResponse({'sucesso': False, 'erro': form.errors}, status=400)

        produto = form.save(commit=False)
        # Se seu form não cobre tudo, resolva fornecedor/área manualmente:
        # produto.fornecedor = Fornecedor.objects.get(id=dados['fornecedor'])
        # produto.area       = Area.objects.get(id=dados['area'])
        produto.save()

        return JsonResponse({'sucesso': True, 'id': produto.id})
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)