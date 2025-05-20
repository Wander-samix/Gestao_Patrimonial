import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_subitem_pedido_service import CriarSubitem_pedidoService

@require_POST
def criar_subitem_pedido(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarSubitem_pedidoService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        subitem = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': subitem.id,
        'pedido_id': subitem.pedido_id,
        'produto_id': subitem.produto_id,
        'quantidade': subitem.quantidade,
        'estoque_no_pedido': subitem.estoque_no_pedido,
    }, status=201)
