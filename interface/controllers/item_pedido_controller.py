import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_item_pedido_service import CriarItem_pedidoService

@require_POST
def criar_item_pedido(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarItem_pedidoService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        item = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': item.id,
        'pedido_id': item.pedido_id,
        'produto_id': item.produto_id,
        'quantidade': item.quantidade,
        'liberado': item.liberado,
        'observacao': item.observacao,
        'estoque_no_pedido': item.estoque_no_pedido,
    }, status=201)
