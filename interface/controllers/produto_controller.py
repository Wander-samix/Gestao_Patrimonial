import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_produto_service import CriarProdutoService

@require_POST
def criar_produto(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarProdutoService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        produto = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': produto.id,
        'nfe_numero': produto.nfe_numero,
        'codigo_barras': produto.codigo_barras,
        'descricao': produto.descricao,
        'fornecedor_id': produto.fornecedor_id,
        'area_id': produto.area_id,
        'lote': produto.lote,
        'validade': produto.validade.isoformat() if produto.validade else None,
        'quantidade': produto.quantidade,
        'quantidade_inicial': produto.quantidade_inicial,
        'preco_unitario': float(produto.preco_unitario),
        'status': produto.status,
        'criado_por_id': produto.criado_por_id,
        'criado_em': produto.criado_em.isoformat() if produto.criado_em else None,
    }, status=201)
