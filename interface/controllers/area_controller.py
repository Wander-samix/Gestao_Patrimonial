from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Area


@login_required
def lista_areas(request):
    areas = Area.objects.all()
    return render(request, 'area/lista.html', {'areas': areas})


@login_required
def nova_area(request):
    if request.method == 'POST':
        data = request.POST.dict()
        Area.objects.create(**data)
        messages.success(request, 'Área cadastrada com sucesso.')
        return redirect(reverse('lista_areas'))
    return render(request, 'area/novo.html')


@login_required
def editar_area(request, id):
    area = get_object_or_404(Area, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            setattr(area, key, value)
        area.save()
        messages.success(request, 'Área atualizada com sucesso.')
        return redirect(reverse('lista_areas'))
    return render(request, 'area/editar.html', {'area': area})


@login_required
def excluir_area(request, id):
    area = get_object_or_404(Area, id=id)
    area.delete()
    messages.success(request, 'Área excluída com sucesso.')
    return redirect(reverse('lista_areas'))
