import csv
import json
import xml.etree.ElementTree as ET
from django.shortcuts   import render, redirect, get_object_or_404
from django.urls        import reverse
from django.http        import HttpResponse, JsonResponse
from django.contrib     import messages
from django.contrib.auth.decorators import login_required
from django.db.models   import Q

from core.models             import Produto, Fornecedor, Area
from interface.forms.forms   import ProdutoForm


@login_required
def lista_produtos(request):
    # Parâmetros de filtro
    busca = request.GET.get('busca', '').strip()
    filtro_area = request.GET.get('filtro_area', '')
    filtro_status = request.GET.get('filtro_status', '')
    estoque_baixo = request.GET.get('estoque_baixo') == '1'

    # Queryset base com relacionamentos
    qs = Produto.objects.select_related('fornecedor', 'area')

    # Total antes de aplicar filtros
    total_produtos = qs.count()

    # Filtrar por busca em descrição ou código de barras
    if busca:
        qs = qs.filter(
            Q(descricao__icontains=busca) |
            Q(codigo_barras__icontains=busca)
        )

    # Filtrar por área
    if filtro_area:
        qs = qs.filter(area__nome=filtro_area)

    # Filtrar por status
    if filtro_status in ['ativo', 'inativo']:
        qs = qs.filter(status=filtro_status)

    # Filtrar apenas estoque baixo
    if estoque_baixo:
        qs = qs.filter(estoque_baixo=True)

    # Total após filtros
    total_filtrados = qs.count()

    # Ordenação final
    produtos = qs.order_by('-criado_em')

    # Dados de áreas e fornecedores para filtros e inline add
    areas = Area.objects.all()
    fornecedores = Fornecedor.objects.all()
    areas_json = list(areas.values('id', 'nome'))
    fornecedores_json = list(fornecedores.values('id', 'nome'))

    return render(request, 'core/lista_produtos.html', {
        'produtos': produtos,
        'areas': areas,
        'fornecedores': fornecedores,
        'areas_json': areas_json,
        'fornecedores_json': fornecedores_json,
        'busca': busca,
        'filtro_area': filtro_area,
        'filtro_status': filtro_status,
        'estoque_baixo_aplicado': estoque_baixo,
        'total_produtos': total_produtos,
        'total_filtrados': total_filtrados,
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
        writer.writerow([p.id, p.descricao, p.quantidade_inicial, p.preco_unitario])
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
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)


@login_required
def salvar_produto_inline(request):
    """
    Recebe JSON com os campos de um produto, cadastra e devolve {sucesso: true}.
    """
    if request.method != 'POST':
        return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'}, status=405)

    try:
        dados = json.loads(request.body)
        form = ProdutoForm(dados)
        if not form.is_valid():
            return JsonResponse({'sucesso': False, 'erro': form.errors}, status=400)

        produto = form.save(commit=False)
        produto.save()
        return JsonResponse({'sucesso': True, 'id': produto.id})
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=500)


@login_required
def cadastro_produtos(request):
    """
    Recebe o POST do template de confirmação (produtos_extraidos.html),
    cadastra cada linha como Produto e redireciona para a lista.
    """
    if request.method != 'POST':
        return redirect(reverse('lista_produtos'))

    codigos     = request.POST.getlist('codigo_barras')
    descricoes  = request.POST.getlist('descricao')
    fornecedores= request.POST.getlist('fornecedor_id')
    lotes       = request.POST.getlist('lote')
    validades   = request.POST.getlist('validade')
    quantidades = request.POST.getlist('quantidade')
    precos      = request.POST.getlist('preco_unitario')
    statuses    = request.POST.getlist('status')

    created = 0
    for i in range(len(codigos)):
        try:
            produto = Produto(
                codigo_barras      = codigos[i],
                descricao          = descricoes[i],
                fornecedor_id      = int(fornecedores[i]) if fornecedores[i] else None,
                lote               = lotes[i],
                validade           = validades[i] or None,
                quantidade_inicial = int(quantidades[i]),
                preco_unitario     = float(precos[i]),
                status             = statuses[i],
            )
            produto.save()
            created += 1
        except Exception:
            continue

    messages.success(request, f'{created} produto(s) importado(s) com sucesso.')
    return redirect(reverse('lista_produtos'))