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


def fornecedores_view(request):
    if request.method == "POST":
        Fornecedor.objects.create(
            nome=request.POST["nome"],
            cnpj=request.POST["cnpj"],
            endereco=request.POST["endereco"],
            telefone=request.POST["telefone"],
            email=request.POST["email"]
        )
    fornecedores = Fornecedor.objects.all()
    return render(request, "core/fornecedores.html", {"fornecedores": fornecedores})

@login_required

def salvar_fornecedor_inline(request):
    try:
        data = json.loads(request.body)
        fornecedor = Fornecedor.objects.create(
            nome     = data.get("nome", ""),
            cnpj     = data.get("cnpj", ""),
            telefone = data.get("telefone", ""),
            email    = data.get("email", ""),
            ativo    = True
        )
        return JsonResponse({"sucesso": True, "id": fornecedor.id})
    except Exception as e:
        return JsonResponse({"sucesso": False, "erro": str(e)})
    
@login_required

def ativar_fornecedor(request, pk):
    f = get_object_or_404(Fornecedor, pk=pk)
    f.ativo = True
    f.save()
    messages.success(request, f"Fornecedor {f.nome} ativado com sucesso.")
    return redirect('fornecedores')


@login_required

def desativar_fornecedor(request, pk):
    f = get_object_or_404(Fornecedor, pk=pk)
    f.ativo = False
    f.save()
    messages.success(request, f"Fornecedor {f.nome} desativado com sucesso.")
    return redirect('fornecedores')


@login_required

def editar_fornecedor(request, pk):
    f = get_object_or_404(Fornecedor, pk=pk)
    if request.method == "POST":
        f.nome      = request.POST["nome"]
        f.cnpj      = request.POST["cnpj"]
        f.endereco  = request.POST.get("endereco", f.endereco)
        f.telefone  = request.POST.get("telefone", f.telefone)
        f.email     = request.POST.get("email", f.email)
        f.save()
        messages.success(request, f"Fornecedor {f.nome} atualizado com sucesso.")
        return redirect('fornecedores')
    return render(request, "core/editar_fornecedor.html", {"fornecedor": f})


# ---------- Usuários ----------

@login_required

def deletar_fornecedor(request, pk):
    f = get_object_or_404(Fornecedor, pk=pk)

    # Verifica vínculos com produtos ativos
    if Produto.objects.filter(fornecedor=f, status='ativo').exists():
        messages.error(
            request,
            "Não foi possível excluir: existem produtos ativos vinculados a este fornecedor."
        )
        return redirect('fornecedores')

    f.delete()
    messages.success(request, f"Fornecedor {f.nome} excluído com sucesso.")
    return redirect('fornecedores')

@csrf_exempt
@require_POST
@login_required

