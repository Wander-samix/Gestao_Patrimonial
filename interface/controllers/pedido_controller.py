from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Pedido


@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/lista.html', {'pedidos': pedidos})


@login_required
def novo_pedido(request):
    if request.method == 'POST':
        data = request.POST.dict()
        Pedido.objects.create(**data)
        messages.success(request, 'Pedido cadastrado com sucesso.')
        return redirect(reverse('lista_pedidos'))
    return render(request, 'pedido/novo.html')


@login_required
def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(pedido, key, value)
        pedido.save()
        messages.success(request, 'Pedido atualizado com sucesso.')
        return redirect(reverse('lista_pedidos'))
    return render(request, 'pedido/editar.html', {'pedido': pedido})


@login_required
def excluir_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.delete()
    messages.success(request, 'Pedido excluído com sucesso.')
    return redirect(reverse('lista_pedidos'))
