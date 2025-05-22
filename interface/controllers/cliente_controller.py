from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Cliente


@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/lista.html', {'clientes': clientes})


@login_required
def novo_cliente(request):
    if request.method == 'POST':
        data = request.POST.dict()
        # mapear campos conforme necessário
        Cliente.objects.create(**data)
        messages.success(request, 'Cliente cadastrado com sucesso.')
        return redirect(reverse('lista_clientes'))
    return render(request, 'cliente/novo.html')


@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(cliente, key, value)
        cliente.save()
        messages.success(request, 'Cliente atualizado com sucesso.')
        return redirect(reverse('lista_clientes'))
    return render(request, 'cliente/editar.html', {'cliente': cliente})


@login_required
def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, 'Cliente excluído com sucesso.')
    return redirect(reverse('lista_clientes'))
