from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import ItemPedido


@login_required
def lista_item_pedidos(request):
    item_pedidos = ItemPedido.objects.all()
    return render(request, 'item_pedido/lista.html', {'item_pedidos': item_pedidos})


@login_required
def novo_item_pedido(request):
    if request.method == 'POST':
        data = request.POST.dict()
        ItemPedido.objects.create(**data)
        messages.success(request, 'Item de pedido cadastrado com sucesso.')
        return redirect(reverse('lista_item_pedidos'))
    return render(request, 'item_pedido/novo.html')


@login_required
def editar_item_pedido(request, id):
    item = get_object_or_404(ItemPedido, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(item, key, value)
        item.save()
        messages.success(request, 'Item de pedido atualizado com sucesso.')
        return redirect(reverse('lista_item_pedidos'))
    return render(request, 'item_pedido/editar.html', {'item_pedido': item})


@login_required
def excluir_item_pedido(request, id):
    item = get_object_or_404(ItemPedido, id=id)
    item.delete()
    messages.success(request, 'Item de pedido excluído com sucesso.')
    return redirect(reverse('lista_item_pedidos'))
