import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from core.application.dtos.saida_produto_por_pedido_dto import CreateSaidaProdutoPorPedidoDTO
from core.application.services.criar_saida_produto_por_pedido_service import SaidaProdutoPorPedidoService

@require_POST
def criar_saida_produto_por_pedido(request):
    # 1) Parse do JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) Monta DTO
    dto = CreateSaidaProdutoPorPedidoDTO(
        produto_id=payload.get('produto_id', 0),
        pedido_id=payload.get('pedido_id', 0),
        quantidade=payload.get('quantidade', 0),
    )

    # 3) Executa o serviço
    service = SaidaProdutoPorPedidoService()
    try:
        out = service.create(dto)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 4) Retorna JSON
    return JsonResponse({
        'id': out.id,
        'produto_id': out.produto_id,
        'pedido_id': out.pedido_id,
        'quantidade': out.quantidade,
        'data_saida': out.data_saida,
    }, status=201)
