from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import LogAcao


@login_required
def lista_logs_acao(request):
    logs_acao = LogAcao.objects.all()
    return render(request, 'log_acao/lista.html', {'logs_acao': logs_acao})


@login_required
def novo_log_acao(request):
    if request.method == 'POST':
        data = request.POST.dict()
        LogAcao.objects.create(**data)
        messages.success(request, 'Log de ação cadastrado com sucesso.')
        return redirect(reverse('lista_logs_acao'))
    return render(request, 'log_acao/novo.html')


@login_required
def editar_log_acao(request, id):
    log = get_object_or_404(LogAcao, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(log, key, value)
        log.save()
        messages.success(request, 'Log de ação atualizado com sucesso.')
        return redirect(reverse('lista_logs_acao'))
    return render(request, 'log_acao/editar.html', {'log_acao': log})


@login_required
def excluir_log_acao(request, id):
    log = get_object_or_404(LogAcao, id=id)
    log.delete()
    messages.success(request, 'Log de ação excluído com sucesso.')
    return redirect(reverse('lista_logs_acao'))
