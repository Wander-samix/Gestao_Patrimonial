from django.shortcuts import render, redirect, get_object_or_404
from core.models import Usuario
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def lista_usuarios(request):
    itens = Usuario.objects.all()
    return render(request, 'usuario/lista.html', {'usuarios': itens})

@login_required
def novo_usuario(request):
    if request.method == 'POST':
        # TODO: map form fields to model fields
        data = request.POST
        Usuario.objects.create(**data.dict())
        messages.success(request, 'Usuario cadastrado com sucesso.')
        return redirect(reverse('lista_usuario'))
    return render(request, 'usuario/novo.html')

@login_required
def editar_usuario(request, id):
    item = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(item, key, value)
        item.save()
        messages.success(request, 'Usuario atualizado com sucesso.')
        return redirect(reverse('lista_usuario'))
    return render(request, 'usuario/editar.html', {'usuario': item})

@login_required
def excluir_usuario(request, id):
    item = get_object_or_404(Usuario, id=id)
    item.delete()
    messages.success(request, 'Usuario excluído com sucesso.')
    return redirect(reverse('lista_usuario'))
