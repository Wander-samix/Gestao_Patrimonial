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


def registrar_movimentacao(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo_barras')
        tipo = request.POST.get('tipo')
        quantidade = int(request.POST.get('quantidade'))
        try:
            produto = Produto.objects.get(codigo_barras=codigo)
        except Produto.DoesNotExist:
            return JsonResponse({'erro': 'Produto não encontrado'}, status=404)
        if tipo == "saida" and produto.quantidade < quantidade:
            return JsonResponse({'erro': 'Estoque insuficiente'}, status=400)
        produto.quantidade = produto.quantidade + quantidade if tipo == "entrada" else produto.quantidade - quantidade
        produto.save()
        MovimentacaoEstoque.objects.create(tipo=tipo, usuario=request.user, quantidade=quantidade, produto=produto)
        return JsonResponse({'mensagem': 'Movimentação registrada com sucesso'})
    return JsonResponse({'erro': 'Método inválido'}, status=405)

@login_required

