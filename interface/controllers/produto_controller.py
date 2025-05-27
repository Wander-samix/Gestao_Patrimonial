# interface/controllers/produto_controller.py

import csv
import json
import xml.etree.ElementTree as ET
from datetime import date, datetime
from itertools import zip_longest

from django.shortcuts            import render, redirect, get_object_or_404
from django.urls                 import reverse
from django.http                 import HttpResponse, JsonResponse
from django.core.files.storage   import FileSystemStorage
from django.contrib              import messages
from django.contrib.auth         import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms   import PasswordChangeForm
from django.core.paginator       import Paginator
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.db                   import transaction
from django.db.models            import Q, Sum, Max, Min, F, DecimalField
from django.db.utils             import IntegrityError
from django.utils.dateparse      import parse_date
from django.utils.timezone       import now
from django.core.mail            import send_mail
from django.core.serializers.json import DjangoJSONEncoder

from openpyxl                    import Workbook
from openpyxl.styles             import Font, Alignment, PatternFill
from openpyxl.utils              import get_column_letter

from core.models import (
    Produto, Fornecedor, Area, ItemPedido, Pedido,
    MovimentacaoEstoque, ConfiguracaoEstoque,
    LogAcao, SessionLog, SaidaProdutoPorPedido
)
from interface.forms.forms import (
    AreaForm, ConfiguracaoEstoqueForm,
    ProfileForm, ProdutoForm
)

User = get_user_model()
PENDING_STATUSES = ['aguardando_aprovacao', 'aprovado', 'separado']


def calcular_estoque_disponivel(codigo_barras, area_id, data_limite=None):
    total = Produto.objects.filter(
        codigo_barras=codigo_barras,
        area_id=area_id
    ).aggregate(s=Sum('quantidade'))['s'] or 0

    reservas = ItemPedido.objects.filter(
        produto__codigo_barras=codigo_barras,
        produto__area_id=area_id,
        pedido__status__in=PENDING_STATUSES
    )
    if data_limite:
        reservas = reservas.filter(pedido__data_solicitacao__date__lte=data_limite)
    reservado = reservas.aggregate(s=Sum('quantidade'))['s'] or 0

    return max(total - reservado, 0)


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
            login(request, user)
            return redirect('lista_produtos')
        messages.error(request, "Credenciais inválidas")
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def lista_produtos(request):
    busca         = request.GET.get('busca', '').strip()
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

    configs = ConfiguracaoEstoque.objects.all()
    minimo_por_area = {cfg.area_id: cfg.estoque_minimo for cfg in configs if cfg.area_id}
    hoje = now().date()

    pendentes = ItemPedido.objects.filter(
        produto__codigo_barras__in=produtos.values_list('codigo_barras', flat=True),
        produto__area_id__in=produtos.values_list('area_id', flat=True),
        pedido__status__in=PENDING_STATUSES
    ).filter(pedido__data_solicitacao__date__lte=hoje)
    reservas = {
        (r['produto__codigo_barras'], r['produto__area_id']): r['total']
        for r in pendentes.values('produto__codigo_barras', 'produto__area_id').annotate(total=Sum('quantidade'))
    }

    produtos_filtrados = []
    for p in produtos.order_by('validade', 'criado_em'):
        key = (p.codigo_barras, p.area_id)
        real     = p.quantidade
        reservado_lote = min(real, reservas.get(key, 0))
        reservas[key] = reservas.get(key, 0) - reservado_lote
        disponivel = real - reservado_lote

        p.estoque_real                     = real
        p.estoque_reservado                = reservado_lote
        p.estoque_disponivel_projetado     = disponivel
        p.estoque_baixo                    = disponivel <= minimo_por_area.get(p.area_id, 0)
        p.percentual_estoque               = (disponivel / minimo_por_area.get(p.area_id, 1)) * 100

        if not somente_baixo or p.estoque_baixo:
            produtos_filtrados.append(p)

    return render(request, 'core/lista_produtos.html', {
        'produtos': produtos_filtrados,
        'busca': busca, 'filtro_status': status, 'filtro_area': filtro_area,
        'ordenar_por': ordenar_por, 'ordem': ordem,
        'areas': Area.objects.all(), 'fornecedores': Fornecedor.objects.all(),
        'estoque_baixo_aplicado': somente_baixo,
    })


@login_required
@require_POST
def upload_nfe(request):
    xml_file = request.FILES.get('arquivo')
    if not xml_file:
        messages.error(request, "Nenhum arquivo enviado.")
        return redirect('cadastro_produtos')

    fs      = FileSystemStorage()
    path    = fs.path(fs.save(xml_file.name, xml_file))
    tree    = ET.parse(path)
    root    = tree.getroot()
    ns      = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    nfe_num = root.findtext('.//nfe:ide/nfe:nNF', namespaces=ns, default='')
    emit    = root.find('.//nfe:emit', ns)
    forn_nm = emit.findtext('nfe:xNome', namespaces=ns, default='')

    itens = []
    for det in root.findall('.//nfe:det', ns):
        prod = det.find('nfe:prod', ns)
        if not prod:
            continue
        itens.append({
            'nfe_numero':      nfe_num,
            'codigo_barras':   prod.findtext('nfe:cProd', namespaces=ns, default=''),
            'descricao':       prod.findtext('nfe:xProd', namespaces=ns, default=''),
            'quantidade':      prod.findtext('nfe:qCom', namespaces=ns, default='0'),
            'preco_unitario':  prod.findtext('nfe:vUnCom', namespaces=ns, default='0.00'),
            'fornecedor_nome': forn_nm,
            'area_id':         None,
        })

    return render(request, 'core/confirmar_importacao.html', {
        'produtos': itens,
        'areas': Area.objects.all(),
        'nfe_numero': nfe_num,
        'fornecedor_nome': forn_nm,
    })


@login_required
def novo_produto(request):
    """
    Se vier mais de um código_barras no POST, faz importação em massa,
    senão usa ProdutoForm para cadastro individual.
    """
    if request.method == "POST":
        cods = request.POST.getlist("codigo_barras")
        # importação em massa
        if len(cods) > 1:
            count = 0
            for cb, desc, fn, aid, val, qt, pu in zip_longest(
                request.POST.getlist("codigo_barras"),
                request.POST.getlist("descricao"),
                request.POST.getlist("fornecedor_nome"),
                request.POST.getlist("area"),
                request.POST.getlist("validade"),
                request.POST.getlist("quantidade"),
                request.POST.getlist("preco_unitario"),
                fillvalue=""
            ):
                validade = parse_date(val) if val else None
                quantidade = int(qt or 0)
                preco       = float(pu or 0)
                fornecedor  = None
                if fn:
                    fornecedor, _ = Fornecedor.objects.get_or_create(nome=fn)

                Produto.objects.create(
                    codigo_barras   = cb,
                    descricao       = desc,
                    fornecedor      = fornecedor,
                    area_id         = aid or None,
                    validade        = validade,
                    quantidade      = quantidade,
                    preco_unitario  = preco,
                    criado_por      = request.user,
                )
                count += 1
            messages.success(request, f"{count} produto(s) importado(s) com sucesso!")
            return redirect('lista_produtos')

        # cadastro individual via form
        form = ProdutoForm(request.POST)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.criado_por = request.user
            prod.save()
            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect('lista_produtos')
        messages.error(request, "Por favor corrija os erros abaixo.")
    else:
        form = ProdutoForm()

    return render(request, "core/cadastro_produtos.html", {
        "form": form,
        "areas": Area.objects.all(),
        "fornecedores": Fornecedor.objects.all(),
    })


@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    form = ProdutoForm(request.POST or None, instance=produto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Produto atualizado com sucesso.")
        return redirect('lista_produtos')
    return render(request, 'core/editar_produto.html', {
        "form": form, "produto": produto
    })


@login_required
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    messages.success(request, "Produto excluído com sucesso.")
    return redirect('lista_produtos')


@csrf_exempt
@login_required
def bulk_delete_produtos(request):
    """
    Recebe JSON {"ids":[...]} e exclui produtos.
    """
    if request.method != 'POST':
        return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'}, status=405)
    try:
        dados = json.loads(request.body)
        ids   = dados.get("ids", [])
        if not isinstance(ids, list):
            raise ValueError("ids deve ser uma lista")
        Produto.objects.filter(id__in=ids).delete()
        return JsonResponse({'sucesso': True})
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)


@csrf_exempt
@login_required
def salvar_produto_inline(request):
    """
    Cadastra um produto via JSON e retorna id.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        fornecedor = Fornecedor.objects.get(id=data['fornecedor'])
        area       = Area.objects.get(id=data['area']) if data.get('area') else None

        iguais = Produto.objects.filter(codigo_barras=data['codigo_barras'])
        lote   = (max(int(p.lote) for p in iguais if p.lote.isdigit()) + 1) if iguais else 1

        produto = Produto.objects.create(
            codigo_barras   = data['codigo_barras'],
            descricao       = data['descricao'],
            fornecedor      = fornecedor,
            area            = area,
            lote            = str(lote),
            validade        = data['validade'],
            quantidade      = int(data['quantidade']),
            preco_unitario  = float(data['preco_unitario']),
            criado_por      = request.user
        )
        return JsonResponse({
            'sucesso': True,
            'id': produto.id,
            'fornecedor_nome': fornecedor.nome,
            'area_nome': area.nome if area else ''
        })
    return JsonResponse({'sucesso': False, 'erro': 'Método inválido'}, status=405)


@login_required
def exportar_produtos_excel(request):
    busca = request.GET.get('busca', '').strip()
    status = request.GET.get('filtro_status', '')
    qs = Produto.objects.select_related('area', 'fornecedor')
    if busca:
        qs = qs.filter(
            Q(descricao__icontains=busca) |
            Q(codigo_barras__icontains=busca)
        )
    if status in ['ativo', 'inativo']:
        qs = qs.filter(status=status)

    wb = Workbook()
    ws = wb.active
    ws.title = "Produtos"

    # Cabeçalho com timestamp
    ts = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    ws.merge_cells('A1:K1')
    cell = ws['A1']
    cell.value = f"Exportado em: {ts}"
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal='right')

    headers = [
        'Código de Barras','Lote','Descrição','Fornecedor','Área',
        'Validade','Quantidade','Estoque Real','Reservado','Disponível','Preço Unitário'
    ]
    header_fill = PatternFill('solid', fgColor="4F81BD")
    header_font = Font(bold=True, color='FFFFFF')
    center = Alignment(horizontal='center', vertical='center', wrap_text=True)
    for idx, title in enumerate(headers, start=1):
        c = ws.cell(row=2, column=idx, value=title)
        c.fill = header_fill
        c.font = header_font
        c.alignment = center

    for row_idx, produto in enumerate(qs, start=3):
        info = calcular_estoque_disponivel(produto.codigo_barras, produto.area_id)
        ws.cell(row=row_idx, column=1, value=produto.codigo_barras)
        ws.cell(row=row_idx, column=2, value=produto.lote)
        ws.cell(row=row_idx, column=3, value=produto.descricao)
        ws.cell(row=row_idx, column=4, value=getattr(produto.fornecedor, 'nome', ''))
        ws.cell(row=row_idx, column=5, value=produto.area.nome if produto.area else "")
        ws.cell(row=row_idx, column=6, value=produto.validade.strftime('%d/%m/%Y') if produto.validade else "")
        ws.cell(row=row_idx, column=7, value=produto.quantidade)
        ws.cell(row=row_idx, column=8, value=info)
        ws.cell(row=row_idx, column=9, value="")
        ws.cell(row=row_idx, column=10, value="")
        ws.cell(row=row_idx, column=11, value=float(produto.preco_unitario))

    for col in ws.columns:
        max_length = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = max_length + 2

    resp = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    resp['Content-Disposition'] = 'attachment; filename="produtos.xlsx"'
    wb.save(resp)
    return resp


@login_required
@user_passes_test(lambda u: u.papel == 'admin')
def deletar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    messages.success(request, "Produto excluído com sucesso.")
    return redirect('lista_produtos')

@login_required
def cadastro_produtos(request):
    """
    Recebe POST de confirmar_importacao e cadastra produtos em massa;
    também trata fallback individual. Ao final, sempre redireciona para lista.
    """
    areas = Area.objects.all()
    fornecedores = Fornecedor.objects.all()

    if request.method == "POST":
        try:
            # --- Importação em massa via NFe ---
            codigos        = request.POST.getlist("codigo_barras")
            descricoes     = request.POST.getlist("descricao")
            nomes_forneced = request.POST.getlist("fornecedor_nome")
            area_ids       = request.POST.getlist("area_id")
            lotes          = request.POST.getlist("lote")
            validades      = request.POST.getlist("validade")
            quantidades    = request.POST.getlist("quantidade")
            precos         = request.POST.getlist("preco_unitario")
            statuses       = request.POST.getlist("status")
            nfe_nums       = request.POST.getlist("nfe_numero")

            # se houver ao menos um código, trata importação em massa
            if any(codigos):
                created = 0
                for (
                    cb, desc, fn, aid, lote, val, qt, pr, st, nfe
                ) in zip_longest(
                    codigos,
                    descricoes,
                    nomes_forneced,
                    area_ids,
                    lotes,
                    validades,
                    quantidades,
                    precos,
                    statuses,
                    nfe_nums,
                    fillvalue=""
                ):
                    # parse de campos
                    validade = parse_date(val) if val else None
                    quantidade     = int(qt)  if qt.strip() else 0
                    preco_unitario = float(pr) if pr.strip() else 0.0
                    status_final   = st or "ativo"

                    # cria ou recupera fornecedor
                    if fn:
                        fornecedor, _ = Fornecedor.objects.get_or_create(nome=fn)
                    else:
                        fornecedor = None

                    Produto.objects.create(
                        nfe_numero      = nfe,
                        codigo_barras   = cb,
                        descricao       = desc,
                        fornecedor      = fornecedor,
                        area_id         = aid or None,
                        lote            = lote,
                        validade        = validade,
                        quantidade      = quantidade,
                        preco_unitario  = preco_unitario,
                        status          = status_final,
                        criado_por      = request.user,
                    )
                    created += 1

                messages.success(request, f"{created} produto(s) importado(s) com sucesso!")
                return redirect("lista_produtos")

            # --- Fallback individual ---
            codigo_barras = request.POST.get("codigo_barras")
            if codigo_barras:
                descricao      = request.POST.get("descricao", "")
                fornecedor_id  = request.POST.get("fornecedor")
                area_id        = request.POST.get("area_id")
                lote           = request.POST.get("lote", "")
                validade_str   = request.POST.get("validade")
                quantidade     = int(request.POST.get("quantidade", 0))
                preco_unitario = float(request.POST.get("preco_unitario", 0))
                status_final   = request.POST.get("status") or "ativo"

                validade = parse_date(validade_str) if validade_str else None

                if not fornecedor_id or not area_id:
                    messages.error(request, "Fornecedor e área são obrigatórios.")
                else:
                    Produto.objects.create(
                        codigo_barras   = codigo_barras,
                        descricao       = descricao,
                        fornecedor_id   = fornecedor_id,
                        area_id         = area_id,
                        lote            = lote,
                        validade        = validade,
                        quantidade      = quantidade,
                        preco_unitario  = preco_unitario,
                        status          = status_final,
                        criado_por      = request.user,
                    )
                    messages.success(request, "Produto cadastrado com sucesso!")
                return redirect("lista_produtos")

        except IntegrityError:
            messages.error(request, "Erro ao cadastrar produto. Verifique os dados.")
            return redirect("cadastro_produtos")

    # GET: exibe formulário de cadastro/importação
    return render(request, "core/cadastro_produtos.html", {
        "areas":        areas,
        "fornecedores": fornecedores,
    })