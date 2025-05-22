from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Fornecedor


@login_required
def lista_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'fornecedor/lista.html', {'fornecedores': fornecedores})


@login_required
def novo_fornecedor(request):
    if request.method == 'POST':
        data = request.POST.dict()
        # mapear campos conforme necessário
        Fornecedor.objects.create(**data)
        messages.success(request, 'Fornecedor cadastrado com sucesso.')
        return redirect(reverse('lista_fornecedores'))
    return render(request, 'fornecedor/novo.html')


@login_required
def editar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(fornecedor, key, value)
        fornecedor.save()
        messages.success(request, 'Fornecedor atualizado com sucesso.')
        return redirect(reverse('lista_fornecedores'))
    return render(request, 'fornecedor/editar.html', {'fornecedor': fornecedor})


@login_required
def excluir_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    fornecedor.delete()
    messages.success(request, 'Fornecedor excluído com sucesso.')
    return redirect(reverse('lista_fornecedores'))
