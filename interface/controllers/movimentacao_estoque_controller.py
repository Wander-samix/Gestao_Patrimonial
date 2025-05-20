import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_movimentacao_estoque_service import CriarMovimentacao_estoqueService

@require_POST
def criar_movimentacao_estoque(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarMovimentacao_estoqueService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        mov = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': mov.id,
        'tipo': mov.tipo,
        'data': mov.data.isoformat(),
        'usuario_id': mov.usuario_id,
        'quantidade': mov.quantidade,
        'produto_id': mov.produto_id,
        'nota_fiscal_id': mov.nota_fiscal_id,
        'cliente_id': mov.cliente_id,
    }, status=201)
