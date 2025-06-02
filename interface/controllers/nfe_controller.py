# interface/controllers/nfe_controller.py

import xml.etree.ElementTree as ET
from decimal import Decimal
from django.shortcuts      import render, redirect, get_object_or_404
from django.urls           import reverse
from django.contrib        import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage      import FileSystemStorage
from datetime import datetime

from core.models import NFe, Fornecedor, Produto, Area
from core.application.services.criar_nfe_service import NfeService
from core.application.dtos.nfe_dto import CreateNfeDTO

@login_required
def lista_nfes(request):
    """
    Exibe todas as NFes persistidas (modelo core.models.NFe).
    """
    nfes = NFe.objects.all().order_by('-data_emissao', '-id')
    return render(request, 'nfe/lista.html', {'nfes': nfes})


@login_required
def nova_nfe(request):
    """
    View para exibir o formulário de upload de XML de NFe.
    - Em GET: devolve a página de upload.
    - Em POST: encaminha para upload_nfe (que faz parsing e renderiza confirmação).
    """
    if request.method == "GET":
        return render(request, 'core/upload_nfe.html')

    # Se for POST, encaminha para a lógica de parsing (upload_nfe).
    return upload_nfe(request)


@login_required
def upload_nfe(request):
    """
    Recebe o XML enviado pelo usuário (/nfe/upload/) e faz o parsing.
    Em seguida, renderiza 'confirmar_importacao.html' para que o usuário escolha área,
    validade etc. para cada item.
    """
    if request.method != "POST":
        messages.error(request, "Método inválido para upload de NFe.")
        return redirect(reverse('nova_nfe'))

    xml_file = request.FILES.get('arquivo')
    if not xml_file:
        messages.error(request, "Por favor, selecione um arquivo XML.")
        return redirect(reverse('nova_nfe'))

    # Salva temporariamente em 'tmp/' para podermos parsear
    fs = FileSystemStorage(location='tmp/')
    filename = fs.save(xml_file.name, xml_file)
    filepath = fs.path(filename)

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Detecta namespace (se houver)
        ns = ''
        if root.tag.startswith('{'):
            ns = root.tag.split('}')[0] + '}'

        # === 1) Extrai cabeçalho da NFe ===
        ide = root.find(f".//{ns}ide")
        # Número da NFe
        nfe_numero = ide.find(f"{ns}nNF").text if ide is not None and ide.find(f"{ns}nNF") is not None else ''
        # Data de emissão (formato YYYY-MM-DD)
        data_emissao_raw = ide.find(f"{ns}dEmi").text if ide is not None and ide.find(f"{ns}dEmi") is not None else None
        data_emissao = datetime.strptime(data_emissao_raw, "%Y-%m-%d").date() if data_emissao_raw else None

        # Totais (vNF e vPeso)
        icmstot = root.find(f".//{ns}ICMSTot")
        valor_total = Decimal(icmstot.find(f"{ns}vNF").text) if icmstot is not None and icmstot.find(f"{ns}vNF") is not None else Decimal('0.00')
        peso = Decimal(icmstot.find(f"{ns}vPeso").text) if icmstot is not None and icmstot.find(f"{ns}vPeso") is not None else Decimal('0.00')

        # Emitente (fornecedor): CNPJ e xNome
        emit = root.find(f".//{ns}emit")
        cnpj_fornecedor = emit.find(f"{ns}CNPJ").text if emit is not None and emit.find(f"{ns}CNPJ") is not None else ''
        nome_fornecedor = emit.find(f"{ns}xNome").text if emit is not None and emit.find(f"{ns}xNome") is not None else ''

        # === 2) Extrai itens (/NFe/infNFe/det) ===
        produtos_extraidos = []
        dets = root.findall(f".//{ns}det")
        for det in dets:
            prod = det.find(f"{ns}prod")
            if prod is None:
                continue

            # cProd (código) e xProd (descrição)
            codigo_barras = prod.find(f"{ns}cProd").text if prod.find(f"{ns}cProd") is not None else ''
            descricao     = prod.find(f"{ns}xProd").text if prod.find(f"{ns}xProd") is not None else ''

            # Quantidade (qCom)
            qt_text = prod.find(f"{ns}qCom").text if prod.find(f"{ns}qCom") is not None else '0'
            quantidade = int(Decimal(qt_text)) if qt_text else 0

            # Valor unitário (vUnCom)
            vuc_text = prod.find(f"{ns}vUnCom").text if prod.find(f"{ns}vUnCom") is not None else '0.00'
            preco_unitario = float(Decimal(vuc_text)) if vuc_text else 0.0

            # Validade (pode não vir no XML)
            validade = ''

            # Lote: em branco, pois será calculado em Produto.save()
            lote = ''

            # Status padrão
            status = "ativo"

            produtos_extraidos.append({
                'codigo_barras':   codigo_barras,
                'descricao':       descricao,
                'fornecedor_nome': nome_fornecedor,
                'quantidade':      quantidade,
                'preco_unitario':  preco_unitario,
                'validade':        validade,
                'lote':            lote,
                'status':          status,
                'area_id':         None,  # o usuário seleciona no template
            })

        # Remove o arquivo temporário
        fs.delete(filename)

        if not produtos_extraidos:
            messages.warning(request, "Nenhum item encontrado no XML da NFe.")
            return redirect(reverse('nova_nfe'))

        # === 3) Renderiza confirmação, enviando cabeçalho + itens ===
        return render(request, 'core/confirmar_importacao.html', {
            'produtos':        produtos_extraidos,
            'areas':           Area.objects.all(),
            'nfe_numero':      nfe_numero,
            'data_emissao':    data_emissao,
            'cnpj_fornecedor': cnpj_fornecedor,
            'valor_total':     valor_total,
            'peso':            peso,
        })

    except ET.ParseError:
        fs.delete(filename)
        messages.error(request, 'Estrutura do XML inválida. Verifique o arquivo e tente novamente.')
        return redirect(reverse('nova_nfe'))


@login_required
def confirmar_nfe(request):
    """
    Recebe o POST do formulário de confirmação (confirmar_importacao.html).
    Em seguida, cria produtos e cria a NFe no banco via NfeService.
    """
    if request.method != "POST":
        messages.error(request, "Acesso inválido para confirmar NFe.")
        return redirect(reverse('lista_nfes'))

    # 1) Coleta os campos getlist() (mesmo que tenhamos multiples linhas)
    lista_codigos      = request.POST.getlist("codigo_barras")
    lista_descricoes   = request.POST.getlist("descricao")
    lista_fornecedores  = request.POST.getlist("fornecedor_nome")
    lista_area_ids     = request.POST.getlist("area_id")
    lista_lotes        = request.POST.getlist("lote")
    lista_validade     = request.POST.getlist("validade")
    lista_quantidades  = request.POST.getlist("quantidade")
    lista_precos       = request.POST.getlist("preco_unitario")
    lista_status       = request.POST.getlist("status")

    # Campos ocultos de cabeçalho
    nfe_numero      = request.POST.get("nfe_numero", "").strip()
    data_emissao_str= request.POST.get("data_emissao", "").strip()
    cnpj_fornecedor = request.POST.get("cnpj_fornecedor", "").strip()
    valor_total_str = request.POST.get("valor_total", "0")
    peso_str        = request.POST.get("peso", "0")

    # Converte data_emissao
    try:
        data_emissao = datetime.strptime(data_emissao_str, "%Y-%m-%d").date()
    except:
        data_emissao = None

    # Converte valor_total e peso
    try:
        valor_total = float(valor_total_str)
    except:
        valor_total = 0.0
    try:
        peso = float(peso_str)
    except:
        peso = 0.0

    # 2) Cria cada Produto e armazena o ID
    produtos_criados_ids = []
    for idx in range(len(lista_codigos)):
        cod       = lista_codigos[idx]
        desc      = lista_descricoes[idx]
        forn_nome = lista_fornecedores[idx]
        area_id   = lista_area_ids[idx]
        lote_val  = lista_lotes[idx]
        validade  = lista_validade[idx]
        quant     = lista_quantidades[idx]
        preco     = lista_precos[idx]
        status    = lista_status[idx]

        # 2.1) Recupera ou cria Fornecedor por CNPJ (ou nome, se não existir)
        fornecedor_obj = None
        if cnpj_fornecedor:
            fornecedor_obj = Fornecedor.objects.filter(cnpj=cnpj_fornecedor).first()
        if not fornecedor_obj:
            fornecedor_obj = Fornecedor.objects.filter(nome__iexact=forn_nome).first()
        if not fornecedor_obj:
            fornecedor_obj = Fornecedor.objects.create(
                nome=forn_nome,
                cnpj=cnpj_fornecedor or None
            )

        # 2.2) Cria o Produto
        produto = Produto(
            nfe_numero     = nfe_numero,
            codigo_barras  = cod,
            descricao      = desc,
            fornecedor     = fornecedor_obj,
            area_id        = area_id or None,
            lote           = None,            # será calculado no save()
            validade       = validade or None,
            quantidade     = int(quant) if quant.isdigit() else 0,
            preco_unitario = float(preco) if preco else 0.0,
            status         = status or 'ativo',
            criado_por     = request.user
        )
        produto.save()  # no save() do modelo, lote = último_lote + 1
        produtos_criados_ids.append(produto.id)

    # 3) Agora cria o cabeçalho da NFe via NfeService
    try:
        create_dto = CreateNfeDTO(
            numero               = nfe_numero,
            data_emissao         = data_emissao,
            cnpj_fornecedor      = cnpj_fornecedor,
            peso                 = peso,
            valor_total          = valor_total,
            itens_vinculados_ids = produtos_criados_ids,
            area_id              = None  # se quiser amarrar a NFe a uma área fixa, coloque aqui
        )
        service = NfeService()
        service.create(create_dto)
    except Exception as e:
        messages.error(request, f"Erro ao registrar NFe: {str(e)}")
        return redirect(reverse('lista_produtos'))

    messages.success(request, f"{len(produtos_criados_ids)} produto(s) importado(s) e NFe '{nfe_numero}' registrada.")
    return redirect(reverse('lista_produtos'))


@login_required
def editar_nfe(request, id):
    """
    View para editar os campos básicos de uma NFe existente (cabecalho).
    Se for GET, exibe um formulário simples com os campos que deseja permitir alterar.
    Se for POST, salva as alterações.
    """
    nfe_obj = get_object_or_404(NFe, pk=id)

    if request.method == "POST":
        # Exemplo: alterar somente número e data_emissao
        numero      = request.POST.get("numero", nfe_obj.numero).strip()
        data_str    = request.POST.get("data_emissao", nfe_obj.data_emissao.strftime("%Y-%m-%d"))
        valor_str   = request.POST.get("valor_total", str(nfe_obj.valor_total))
        peso_str    = request.POST.get("peso", str(nfe_obj.peso))

        # Converte data
        try:
            data_emissao = datetime.strptime(data_str, "%Y-%m-%d").date()
        except:
            data_emissao = nfe_obj.data_emissao

        # Converte valor_total e peso
        try:
            valor_total = float(valor_str)
        except:
            valor_total = float(nfe_obj.valor_total)
        try:
            peso = float(peso_str)
        except:
            peso = float(nfe_obj.peso)

        # Atualiza campos
        nfe_obj.numero         = numero
        nfe_obj.data_emissao   = data_emissao
        nfe_obj.valor_total    = valor_total
        nfe_obj.peso           = peso
        nfe_obj.save()

        messages.success(request, f"NFe '{nfe_obj.numero}' atualizada.")
        return redirect(reverse('lista_nfes'))

    # Se for GET, exibe o formulário de edição
    return render(request, 'nfe/editar.html', {'nfe': nfe_obj})


@login_required
def excluir_nfe(request, id):
    """
    Deleta a NFe de ID fornecido e redireciona para a lista.
    """
    nfe_obj = get_object_or_404(NFe, pk=id)
    numero = nfe_obj.numero
    nfe_obj.delete()
    messages.success(request, f"NFe '{numero}' excluída.")
    return redirect(reverse('lista_nfes'))
