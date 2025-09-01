# interface/controllers/login_controller.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import template

register = template.Library()
User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('lista_produtos')
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            # Verifica o boolean 'ativo'
            if getattr(user, 'ativo', False):
                login(request, user)
                return redirect('lista_produtos')
            else:
                return render(request, 'core/login.html', {
                    'error': 'Usuário inativo. Contate o administrador.'
                })
        return render(request, 'core/login.html', {
            'error': 'Credenciais inválidas'
        })
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
