import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from core.application.dtos.subitem_pedido_dto import CreateSubitemPedidoDTO
from core.application.services.criar_subitem_pedido_service import SubitemPedidoService

@require_POST
def criar_subitem_pedido(request):
    # 1) Parse JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) Monta o DTO de entrada
    dto = CreateSubitemPedidoDTO(
        pedido_id        = payload.get('pedido_id', 0),
        produto_id       = payload.get('produto_id', 0),
        quantidade       = payload.get('quantidade', 0),
        estoque_no_pedido= payload.get('estoque_no_pedido'),
    )

    # 3) Chama o serviço
    service = SubitemPedidoService()
    try:
        out = service.create(dto)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 4) Retorna JSON 201
    return JsonResponse({
        'id':               out.id,
        'pedido_id':        out.pedido_id,
        'produto_id':       out.produto_id,
        'quantidade':       out.quantidade,
        'estoque_no_pedido':out.estoque_no_pedido,
    }, status=201)
