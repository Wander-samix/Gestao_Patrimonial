from django.shortcuts import render, redirect, get_object_or_404
from core.models import ConfiguracaoEstoque
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def lista_configuracao_estoque(request):
    itens = ConfiguracaoEstoque.objects.all()
    return render(request, 'configuracao_estoque/lista.html', {'configuracao_estoques': itens})

@login_required
def novo_configuracao_estoque(request):
    if request.method == 'POST':
        # TODO: map form fields to model fields
        data = request.POST
        ConfiguracaoEstoque.objects.create(**data.dict())
        messages.success(request, 'ConfiguracaoEstoque cadastrado com sucesso.')
        return redirect(reverse('lista_configuracao_estoque'))
    return render(request, 'configuracao_estoque/novo.html')

@login_required
def editar_configuracao_estoque(request, id):
    item = get_object_or_404(ConfiguracaoEstoque, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(item, key, value)
        item.save()
        messages.success(request, 'ConfiguracaoEstoque atualizado com sucesso.')
        return redirect(reverse('lista_configuracao_estoque'))
    return render(request, 'configuracao_estoque/editar.html', {'configuracao_estoque': item})

@login_required
def excluir_configuracao_estoque(request, id):
    item = get_object_or_404(ConfiguracaoEstoque, id=id)
    item.delete()
    messages.success(request, 'ConfiguracaoEstoque excluído com sucesso.')
    return redirect(reverse('lista_configuracao_estoque'))
