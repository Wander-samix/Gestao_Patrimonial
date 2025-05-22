from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Produto


@login_required
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/lista_produtos.html', {'produtos': produtos})


@login_required
def novo_produto(request):
    if request.method == 'POST':
        data = request.POST.dict()
        # aqui você pode mapear ou filtrar fields se precisar:
        Produto.objects.create(**data)
        messages.success(request, 'Produto cadastrado com sucesso.')
        return redirect(reverse('lista_produtos'))
    return render(request, 'core/cadastro_produtos.html', {'form': form})


@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(produto, key, value)
        produto.save()
        messages.success(request, 'Produto atualizado com sucesso.')
        return redirect(reverse('lista_produtos'))
    return render(request, 'core/editar_produto.html', {'form': form, 'produto': produto})


@login_required
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    messages.success(request, 'Produto excluído com sucesso.')
    return redirect(reverse('lista_produtos'))
