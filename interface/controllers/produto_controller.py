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


def lista_produtos(request):
    busca         = request.GET.get('busca', '')
    status        = request.GET.get('filtro_status', '')
    filtro_area   = request.GET.get('filtro_area', '')
    ordenar_por   = request.GET.get('ordenar_por', 'id')
    ordem         = request.GET.get('ordem', 'asc')
    somente_baixo = request.GET.get('estoque_baixo') == '1'

    produtos = Produto.objects.all()
    if busca:
        produtos = produtos.filter(
            Q(descricao__icontains=busca) |
            Q(codigo_barras__icontains=busca)
        )
    if status:
        produtos = produtos.filter(status=status)
    if filtro_area:
        produtos = produtos.filter(area__nome__iexact=filtro_area)
    if ordenar_por in ['id', 'validade', 'descricao', 'criado_em']:
        exp = f"-{ordenar_por}" if ordem == 'desc' else ordenar_por
        produtos = produtos.order_by(exp)

    # pega o mínimo configurado por área
    configs = ConfiguracaoEstoque.objects.all()
    minimo_por_area = {
        cfg.area_id: cfg.estoque_minimo
        for cfg in configs if cfg.area_id is not None
    }

    hoje = now().date()

    # 0) total reservado por (codigo_barras, area_id)
    pendentes = ItemPedido.objects.filter(
        produto__codigo_barras__in=produtos.values_list('codigo_barras', flat=True),
        produto__area_id__in=produtos.values_list('area_id', flat=True),
        pedido__status__in=PENDING_STATUSES
    )
    pendentes = pendentes.filter(pedido__data_solicitacao__date__lte=hoje)
    reservas_por_combo = {
        (r['produto__codigo_barras'], r['produto__area_id']): r['total']
        for r in pendentes
                 .values('produto__codigo_barras', 'produto__area_id')
                 .annotate(total=Sum('quantidade'))
    }

    produtos_filtrados = []

    # 1) itera lote a lote, usando p.quantidade como estoque real
    for p in produtos.order_by('validade', 'criado_em'):
        # dias até vencer e mínimo
        p.dias_para_vencer = (p.validade - hoje).days if p.validade else 9999
        p.minimo_area      = minimo_por_area.get(p.area_id, 0)

        key = (p.codigo_barras, p.area_id)
        reservado_restante = reservas_por_combo.get(key, 0)

        # estoque real por lote
        real = p.quantidade

        # reserva alocada a este lote
        reservado_lote = min(real, reservado_restante)
        reservas_por_combo[key] = reservado_restante - reservado_lote

        # disponível projetado do lote
        disponivel = real - reservado_lote

        # atribuições para template
        p.estoque_real                 = real
        p.estoque_reservado            = reservado_lote
        p.estoque_disponivel_projetado = disponivel

        p.estoque_baixo = (
            disponivel <= p.minimo_area
            and p.minimo_area > 0
        )
        p.percentual_estoque = (
            (disponivel / p.minimo_area) * 100
            if p.minimo_area else 100
        )

        if not somente_baixo or p.estoque_baixo:
            produtos_filtrados.append(p)

    context = {
        'produtos': produtos_filtrados,
        'busca': busca,
        'filtro_status': status,
        'filtro_area': filtro_area,
        'ordenar_por': ordenar_por,
        'ordem': ordem,
        'total_produtos': Produto.objects.count(),
        'total_filtrados': len(produtos_filtrados),
        'areas': list(Area.objects.values('id', 'nome')),
        'fornecedores': list(Fornecedor.objects.values('id', 'nome')),
        'estoque_baixo_aplicado': somente_baixo,
    }
    return render(request, 'core/lista_produtos.html', context)



    context = {
        'produtos': produtos_filtrados,
        'busca': busca,
        'filtro_status': status,
        'filtro_area': filtro_area,
        'ordenar_por': ordenar_por,
        'ordem': ordem,
        'total_produtos': Produto.objects.count(),
        'total_filtrados': len(produtos_filtrados),
        'areas': list(Area.objects.values('id', 'nome')),
        'fornecedores': list(Fornecedor.objects.values('id', 'nome')),
        'estoque_baixo_aplicado': somente_baixo,
    }
    return render(request, 'core/lista_produtos.html', context)


    context = {
        'produtos': produtos_filtrados,
        'busca': busca,
        'filtro_status': status,
        'filtro_area': filtro_area,
        'ordenar_por': ordenar_por,
        'ordem': ordem,
        'total_produtos': Produto.objects.count(),
        'total_filtrados': len(produtos_filtrados),
        'areas': list(Area.objects.values('id', 'nome')),
        'fornecedores': list(Fornecedor.objects.values('id', 'nome')),
        'estoque_baixo_aplicado': somente_baixo,
    }
    return render(request, 'core/lista_produtos.html', context)



@login_required

def cadastro_produtos(request):
    areas = Area.objects.all()
    fornecedores = Fornecedor.objects.all()

    if request.method == "POST":
        try:
            # --- Importação em massa via confirmação de NFe ---
            codigos        = request.POST.getlist("codigo_barras")
            if codigos:
                descricoes     = request.POST.getlist("descricao")
                nomes_forneced = request.POST.getlist("fornecedor_nome")
                area_ids       = request.POST.getlist("area")
                validades      = request.POST.getlist("validade")
                quantidades    = request.POST.getlist("quantidade")
                precos         = request.POST.getlist("preco_unitario")
                statuses       = request.POST.getlist("status")
                nfe_numeros    = request.POST.getlist("nfe_numero")

                # iterar sem estourar índice
                for idx, (cb, desc, f_nome, aid, v_str, q_str, p_str, st) in enumerate(
                    zip_longest(
                        codigos, descricoes, nomes_forneced, area_ids,
                        validades, quantidades, precos, statuses,
                        fillvalue=None
                    )
                ):
                    validade = parse_date(v_str) if v_str else None
                    quantidade = int(q_str) if q_str else 0
                    preco_unitario = float(p_str) if p_str else 0.0
                    status = st or "ativo"
                    nfe_numero = nfe_numeros[idx] if idx < len(nfe_numeros) else ""

                    # busca ou cria fornecedor
                    if f_nome:
                        fornecedor, _ = Fornecedor.objects.get_or_create(nome=f_nome)
                    else:
                        fornecedor = None

                    produto = Produto(
                        nfe_numero      = nfe_numero,
                        codigo_barras   = cb or "",
                        descricao       = desc or "",
                        fornecedor      = fornecedor,
                        area_id         = aid or None,
                        validade        = validade,
                        quantidade      = quantidade,
                        preco_unitario  = preco_unitario,
                        status          = status,
                        criado_por      = request.user,
                    )
                    produto.save()

                messages.success(request, "Produtos importados com sucesso!")
                return redirect("lista_produtos")

            # --- Cadastro individual (fallback) ---
            codigo_barras = request.POST.get("codigo_barras")
            if codigo_barras:
                descricao      = request.POST.get("descricao", "")
                fornecedor_id  = request.POST.get("fornecedor")
                area_id        = request.POST.get("area")
                validade       = parse_date(request.POST.get("validade")) or None
                quantidade     = int(request.POST.get("quantidade", 0))
                preco_unitario = float(request.POST.get("preco_unitario", 0))
                status         = request.POST.get("status") or "ativo"

                if not fornecedor_id or not area_id:
                    messages.error(request, "Fornecedor e área são obrigatórios.")
                    return redirect("cadastro_produtos")

                produto = Produto(
                    codigo_barras   = codigo_barras,
                    descricao       = descricao,
                    fornecedor_id   = fornecedor_id,
                    area_id         = area_id,
                    validade        = validade,
                    quantidade      = quantidade,
                    preco_unitario  = preco_unitario,
                    status          = status,
                    criado_por      = request.user,
                )
                produto.save()

                messages.success(request, "Produto cadastrado com sucesso!")
                return redirect("lista_produtos")

        except IntegrityError:
            messages.error(request, "Erro ao cadastrar produto. Verifique os dados.")
            return redirect("cadastro_produtos")

    # GET: exibe formulário de cadastro/importação
    return render(request, "core/cadastro_produtos.html", {
        "fornecedores": fornecedores,
        "areas": areas,
    })

@csrf_exempt
@login_required

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    form = ProdutoForm(request.POST or None, instance=produto)
    if form.is_valid():
        form.save()
        return redirect('lista_produtos')
    return render(request, 'core/editar_produto.html', {
        'form': form, 'produto': produto
    })

def deletar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    messages.success(request, "Produto excluído com sucesso.")
    return redirect('lista_produtos')

# ---------- Cosmos API ----------

def salvar_produto_inline(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            fornecedor = Fornecedor.objects.get(id=dados['fornecedor'])
            area = Area.objects.get(id=dados['area']) if dados.get('area') else None

            produtos_iguais = Produto.objects.filter(codigo_barras=dados['codigo_barras'])
            if produtos_iguais.exists():
                maior_lote = max([int(p.lote) for p in produtos_iguais if str(p.lote).isdigit()] or [0])
                lote = maior_lote + 1
            else:
                lote = 1

            produto = Produto.objects.create(
                codigo_barras=dados['codigo_barras'],
                descricao=dados['descricao'],
                fornecedor=fornecedor,
                area=area,
                lote=str(lote),
                validade=dados['validade'],
                quantidade=int(dados['quantidade']),
                preco_unitario=float(dados['preco_unitario']),
                criado_por=request.user
            )

            return JsonResponse({
                'sucesso': True,
                'id': produto.id,
                'fornecedor_nome': fornecedor.nome,
                'area_nome': area.nome if area else '',
            })

        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)})

    return JsonResponse({'sucesso': False, 'erro': 'Método inválido'})

def buscar_nome_produto_view(request, codigo):
    nome = buscar_nome_produto_por_codigo(codigo)
    return JsonResponse({"codigo": codigo, "nome_produto": nome})

@csrf_exempt
@login_required

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

def upload_nfe(request):
    if request.method == "POST" and request.FILES.get("arquivo"):
        xml_file = request.FILES["arquivo"]
        fs = FileSystemStorage()
        filepath = fs.path(fs.save(xml_file.name, xml_file))
        tree = ET.parse(filepath)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # 1) EXTRAIR O NÚMERO DA NFe
        nfe_numero = root.findtext(".//nfe:ide/nfe:nNF", default="", namespaces=ns)

        # 2) DADOS DO EMITENTE
        emitente = root.find(".//nfe:emit", ns)
        fornecedor_nome = emitente.findtext("nfe:xNome", default="", namespaces=ns)
        fornecedor_cnpj  = emitente.findtext("nfe:CNPJ", default="", namespaces=ns)
        fornecedor, _ = Fornecedor.objects.get_or_create(
            cnpj=fornecedor_cnpj,
            defaults={"nome": fornecedor_nome, "endereco":"", "telefone":"", "email":""}
        )

        # 3) ITENS
        produtos_extraidos = []
        for det in root.findall(".//nfe:det", ns):
            prod = det.find("nfe:prod", ns)
            if prod is None:
                continue
            produtos_extraidos.append({
                "nfe_numero":      nfe_numero,
                "codigo_barras":   prod.findtext("nfe:cProd",  default="", namespaces=ns),
                "descricao":       prod.findtext("nfe:xProd",  default="", namespaces=ns),
                "quantidade":      prod.findtext("nfe:qCom",   default="0",  namespaces=ns),
                "preco_unitario":  prod.findtext("nfe:vUnCom", default="0.00", namespaces=ns),
                "lote":            "",
                "validade":        "",
                "status":          "ativo",
                "fornecedor_nome": fornecedor.nome,     # passa o nome, não o ID
                "area_id":         None,                # será selecionada no template
            })

        return render(request, "core/confirmar_importacao.html", {
            "produtos":    produtos_extraidos,
            "areas":       Area.objects.all(),
            "nfe_numero":  nfe_numero,
        })

    return render(request, "core/upload_nfe.html")


@login_required

def exportar_produtos_excel(request):
    busca = request.GET.get("busca")
    status = request.GET.get("filtro_status")
    produtos = Produto.objects.all()

    if busca:
        produtos = produtos.filter(
            Q(descricao__icontains=busca) |
            Q(codigo_barras__icontains=busca)
        )
    if status:
        produtos = produtos.filter(status=status)

    wb = Workbook()
    ws = wb.active
    ws.title = "Produtos"

    # 1) Carimbo de data/hora na primeira linha
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=13)
    cell_stamp = ws.cell(row=1, column=1, value=f"Exportado em: {timestamp}")
    cell_stamp.font = Font(bold=True)
    cell_stamp.alignment = Alignment(horizontal="right")

    # 2) Cabeçalho (linha 2)
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="4F81BD")
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)

    headers = [
        "Código de Barras", "Lote", "Descrição", "Fornecedor", "Área",
        "Validade", "Quantidade", "Estoque Real", "Reservado", "Disponível",
        "Preço Unitário", "Usuário", "Data de Cadastro"
    ]
    for col_num, col_name in enumerate(headers, start=1):
        cell = ws.cell(row=2, column=col_num, value=col_name)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center

    # 3) Dados dos produtos (a partir da linha 3)
    for idx, produto in enumerate(produtos, start=3):
        info = produto.estoque_info(data_limite=None)  # ou passe data se desejar histórico
        ws.cell(row=idx, column=1, value=produto.codigo_barras)
        ws.cell(row=idx, column=2, value=produto.lote)
        ws.cell(row=idx, column=3, value=produto.descricao)
        ws.cell(row=idx, column=4, value=getattr(produto.fornecedor, 'nome', ''))
        ws.cell(row=idx, column=5, value=produto.area.nome if produto.area else "")
        ws.cell(row=idx, column=6, value=produto.validade.strftime('%d/%m/%Y') if produto.validade else "")
        ws.cell(row=idx, column=7, value=produto.quantidade)
        ws.cell(row=idx, column=8, value=info['real'])
        ws.cell(row=idx, column=9, value=info['reservado'])
        ws.cell(row=idx, column=10, value=info['disponivel'])
        ws.cell(row=idx, column=11, value=float(produto.preco_unitario))
        ws.cell(row=idx, column=12, value=produto.criado_por.username if produto.criado_por else "")
        ws.cell(row=idx, column=13, value=produto.criado_em.strftime('%d/%m/%Y %H:%M') if produto.criado_em else "")

    # 4) Ajustar largura das colunas
    for col in ws.columns:
        max_length = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = max_length + 2

    # 5) Resposta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=produtos.xlsx'
    wb.save(response)
    return response

@login_required

def produtos_por_area(request, area_id):
    qs = Produto.objects.filter(area_id=area_id, status="ativo")

    grouped = (
        qs.values("codigo_barras", "area_id")
          .annotate(
             produto_id    = Max("id"),
             descricao     = Max("descricao"),
             validade      = Min("validade"),
             total_estoque = Sum("quantidade")
          )
    )

    data = []
    for item in grouped:
        disponivel = calcular_estoque_disponivel(item["codigo_barras"], item["area_id"])
        if disponivel <= 0:
            continue

        data.append({
            "id":         item["produto_id"],
            "descricao":  item["descricao"],
            "validade":   item["validade"].strftime("%Y-%m-%d") if item["validade"] else "",
            "disponivel": disponivel,
        })

    return JsonResponse(data, safe=False)


@login_required

def bulk_delete_produtos(request):
    """
    Recebe via POST um JSON { "ids": [1,2,3,...] }
    e deleta todos os produtos cujo id esteja nessa lista.
    """
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            ids = dados.get('ids', [])
            if not isinstance(ids, list):
                raise ValueError("ids deve ser uma lista")
            Produto.objects.filter(id__in=ids).delete()
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)
    return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'}, status=405)

@register.filter

