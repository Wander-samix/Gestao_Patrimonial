# interface/controllers/nfe_controller.py

import xml.etree.ElementTree as ET
from django.shortcuts   import render, redirect, get_object_or_404
from django.urls        import reverse
from django.contrib     import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from core.models import NFe, Fornecedor, Area


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


@login_required
def upload_nfe(request):
    """
    GET:  exibe formulário de upload em core/upload_nfe.html
    POST: processa o XML, extrai os produtos e renderiza core/confirmar_importacao.html
    """
    if request.method == 'GET':
        return render(request, 'core/upload_nfe.html')

    # POST chegando aqui
    arquivo = request.FILES.get('arquivo')
    if not arquivo:
        messages.error(request, 'Selecione um XML de NFe para importar.')
        return redirect(reverse('upload_nfe'))

    # salva temporariamente no disco
    fs = FileSystemStorage()
    nome_arquivo = fs.save(arquivo.name, arquivo)
    caminho = fs.path(nome_arquivo)

    try:
        tree = ET.parse(caminho)
        root = tree.getroot()
        # namespace padrão de NF-e
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # 1) número da NFe
        nfe_numero = root.findtext('.//nfe:ide/nfe:nNF', default='', namespaces=ns)

        # 2) extrai cada <det>
        produtos_extraidos = []
        for det in root.findall('.//nfe:det', ns):
            prod = det.find('nfe:prod', ns)
            if prod is None:
                continue
            produtos_extraidos.append({
                'nfe_numero':     nfe_numero,
                'codigo_barras':  prod.findtext('nfe:cProd',  default='', namespaces=ns),
                'descricao':      prod.findtext('nfe:xProd',  default='', namespaces=ns),
                'quantidade':     prod.findtext('nfe:qCom',   default='0',  namespaces=ns),
                'preco_unitario': prod.findtext('nfe:vUnCom', default='0.00', namespaces=ns),
                'lote':           '',
                'validade':       '',
                'status':         'ativo',
                'fornecedor_nome': '',    # ou extraia do emitente
                'area_id':        None,
            })

        # renderiza tela de confirmação (template já existente)
        return render(request, 'core/confirmar_importacao.html', {
            'produtos':   produtos_extraidos,
            'areas':      Area.objects.all(),
            'nfe_numero': nfe_numero,
        })

    except ET.ParseError:
        messages.error(request, 'XML inválido.')
        return redirect(reverse('upload_nfe'))
