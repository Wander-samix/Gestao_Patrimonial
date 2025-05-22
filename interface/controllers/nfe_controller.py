from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import NFe


@login_required
def lista_nfes(request):
    nfes = NFe.objects.all()
    return render(request, 'nfe/lista.html', {'nfes': nfes})


@login_required
def nova_nfe(request):
    if request.method == 'POST':
        data = request.POST.dict()
        NFe.objects.create(**data)
        messages.success(request, 'NFe cadastrado com sucesso.')
        return redirect(reverse('lista_nfes'))
    return render(request, 'nfe/novo.html')


@login_required
def editar_nfe(request, id):
    nfe = get_object_or_404(NFe, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(nfe, key, value)
        nfe.save()
        messages.success(request, 'NFe atualizado com sucesso.')
        return redirect(reverse('lista_nfes'))
    return render(request, 'nfe/editar.html', {'nfe': nfe})


@login_required
def excluir_nfe(request, id):
    nfe = get_object_or_404(NFe, id=id)
    nfe.delete()
    messages.success(request, 'NFe excluído com sucesso.')
    return redirect(reverse('lista_nfes'))
