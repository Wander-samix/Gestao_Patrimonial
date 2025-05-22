from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.utils import IntegrityError
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models.functions import TruncMonth
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
import xml.etree.ElementTree as ET
import json
import requests
from openpyxl import Workbook
from django.db.models import Q, Sum, Max, Min, F, DecimalField
from django.views.decorators.http import require_GET
from itertools import zip_longest
from core.models import (
    Produto, Fornecedor, Usuario, MovimentacaoEstoque,
    Area, Pedido, ItemPedido, LogAcao,
    ConfiguracaoEstoque)
from ..forms.forms import AreaForm, ConfiguracaoEstoqueForm
from django.db import transaction
from django import template
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from ..forms.forms import ProfileForm
from ..forms.forms import ProdutoForm
import csv
from datetime import date, datetime
from django.shortcuts import render
from core.models import SessionLog
from django.core.paginator import Paginator
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from django.db.models import OuterRef, Subquery
from core.models import SaidaProdutoPorPedido


register = template.Library()
User = get_user_model()

PENDING_STATUSES = [
    'aguardando_aprovacao',
    'aprovado',
    'separado',
]


def lista_usuarios(request):
    usuarios = User.objects.all()
    areas = Area.objects.all()
    return render(request, 'core/usuarios.html', {
        'usuarios': usuarios,
        'areas': areas,
        'total_areas': areas.count(),  
    })

@login_required

def salvar_usuario_inline(request):
    try:
        data = json.loads(request.body)
        
        # Verifica se o usuário já existe
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'sucesso': False, 'erro': 'Usuário já existe'})

        # Cria o usuário com senha padrão
        u = User.objects.create_user(
            username=data['username'],
            email=data.get('email', ''),
            password='senha123'
        )

        # Atribui matrícula
        u.matricula = data.get('matricula', '')

        # Mapeia papéis aceitos com variações
        papel_recebido = data.get('papel', '').strip().lower()
        mapa_papeis = {
            'admin': 'admin',
            'administrador': 'admin',
            'operador': 'operador',
            'técnico': 'tecnico',  # com acento
            'tecnico': 'tecnico',  # sem acento
        }

        papel_final = mapa_papeis.get(papel_recebido)
        if not papel_final:
            return JsonResponse({'sucesso': False, 'erro': 'Papel inválido ou não selecionado'})

        u.papel = papel_final

        # Associa áreas
        area_ids = data.get('areas', [])
        if 'all' in area_ids or u.papel in ['admin', 'tecnico']:
            u.areas.set(Area.objects.values_list('id', flat=True))
        else:
            u.areas.set(area_ids)

        u.save()
        return JsonResponse({'sucesso': True})
    
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)})


@login_required

def ativar_usuario(request, usuario_id):
    if not request.user.is_superuser:
        messages.error(request, "Somente administradores podem ativar usuários.")
        return redirect('lista_usuarios')
    u = get_object_or_404(User, id=usuario_id)
    u.ativo = True
    u.save()
    messages.success(request, f"Usuário {u.username} ativado com sucesso.")
    return redirect('lista_usuarios')

@login_required

def desativar_usuario(request, usuario_id):
    if not request.user.is_superuser:
        messages.error(request, "Somente administradores podem desativar usuários.")
        return redirect('lista_usuarios')

    u = get_object_or_404(User, id=usuario_id)

    if u.papel.lower() == 'admin':
        total_admins_ativos = User.objects.filter(papel__iexact='admin', ativo=True).count()
        if total_admins_ativos <= 1:
            messages.error(request, "Não é possível desativar o único administrador ativo do sistema.")
            return redirect('lista_usuarios')

    u.ativo = False
    u.save()
    messages.success(request, f"Usuário {u.username} desativado com sucesso.")
    return redirect('lista_usuarios')


@login_required

def editar_usuario(request, usuario_id):
    u = get_object_or_404(User, id=usuario_id)
    if request.method == "POST":
        u.username  = request.POST["username"]
        u.email     = request.POST["email"]
        u.matricula = request.POST["matricula"]
        u.papel     = request.POST["papel"]
        # recebe lista de áreas
        area_ids = request.POST.getlist("areas")
        u.save()
        u.areas.set(area_ids)          # atualiza M2M
        messages.success(request, f"Usuário {u.username} atualizado com sucesso.")
        return redirect('lista_usuarios')

    return render(request, 'core/editar_usuario.html', {
        'usuario': u,
        'areas':   Area.objects.all()
    })

@login_required

def deletar_usuario(request, usuario_id):
    if not request.user.is_superuser:
        messages.error(request, "Somente administradores podem excluir usuários.")
        return redirect('lista_usuarios')
    
    u = get_object_or_404(User, id=usuario_id)

    if u.papel.lower() == 'admin':
        total_admins = User.objects.filter(papel__iexact='admin').count()
        if total_admins <= 1:
            messages.error(request, "Não é possível excluir o único administrador do sistema.")
            return redirect('lista_usuarios')

    u.delete()
    messages.success(request, f"Usuário {u.username} excluído com sucesso.")
    return redirect('lista_usuarios')


@csrf_exempt
@require_POST
@login_required

def editar_perfil(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect('editar_perfil')
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'core/editar_perfil.html', {
        'form': form
    })

@login_required

