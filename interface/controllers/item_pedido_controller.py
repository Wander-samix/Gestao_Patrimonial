import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.dtos.item_pedido_dto import CreateItemPedidoDTO
from core.application.services.criar_item_pedido_service import ItemPedidoService
from core.application.contracts.item_pedido_service_contract import IItemPedidoService

@require_POST
def criar_item_pedido(request):
    # 1) Parse do JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) Construção do DTO de entrada
    try:
        dto_in = CreateItemPedidoDTO(
            pedido_id=payload.get('pedido_id'),
            produto_id=payload.get('produto_id'),
            quantidade=payload.get('quantidade'),
            liberado=payload.get('liberado'),
            observacao=payload.get('observacao', ''),
            estoque_no_pedido=payload.get('estoque_no_pedido'),
        )
    except TypeError as e:
        return JsonResponse({'error': f'Campo ausente ou formato inválido: {e}'}, status=400)

    # 3) Chamada do serviço via contrato
    service: IItemPedidoService = ItemPedidoService()
    try:
        dto_out = service.create(dto_in)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 4) Resposta com DTO de saída
    return JsonResponse(dto_out.__dict__, status=201)
