# interface/controllers/nfe_controller.py

import xml.etree.ElementTree as ET
from django.shortcuts   import render, redirect, get_object_or_404
from django.urls        import reverse
from django.contrib     import messages
from django.contrib.auth.decorators import login_required

from core.models import NFe


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
    GET: mostra o form de upload (em core/upload_nfe.html)
    POST: parseia o XML, extrai produtos e renderiza core/produtos_extraidos.html
    """
    if request.method == 'GET':
        return render(request, 'core/upload_nfe.html')

    # agora buscamos o arquivo pelo name="arquivo" do seu form
    arquivo = request.FILES.get('arquivo')
    if not arquivo:
        messages.error(request, 'Selecione um XML de NFe para importar.')
        return redirect(reverse('upload_nfe'))

    try:
        tree = ET.parse(arquivo)
        root = tree.getroot()

        produtos = []
        # percorre os detalhes do XML (ajuste o XPath se necessário)
        for det in root.findall('.//det'):
            prod = det.find('prod')
            produtos.append({
                'codigo_barras':   prod.findtext('cProd', ''),
                'descricao':       prod.findtext('xProd', ''),
                'fornecedor_id':   prod.findtext('cProd', ''),  # ajuste conforme seu modelo
                'lote':            '',
                'validade':        '',
                'quantidade':      prod.findtext('qCom', ''),
                'preco_unitario':  prod.findtext('vUnCom', ''),
                'status':          'ativo',
            })

        return render(request, 'core/produtos_extraidos.html', {
            'produtos': produtos
        })

    except ET.ParseError:
        messages.error(request, 'XML inválido.')
        return redirect(reverse('upload_nfe'))
