import json
from datetime import date
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from core.application.dtos.pedido_dto import CreatePedidoDTO
from core.application.services.criar_pedido_service import PedidoService

@require_POST
def criar_pedido(request):
    # 1) parse JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) converte data_necessaria se for string
    data_raw = payload.get('data_necessaria')
    if isinstance(data_raw, str):
        try:
            payload['data_necessaria'] = date.fromisoformat(data_raw)
        except ValueError:
            return JsonResponse({'error': "Formato de 'data_necessaria' inválido, use YYYY-MM-DD."}, status=400)

    # 3) monta o DTO
    dto = CreatePedidoDTO(
        codigo=payload.get('codigo', ''),
        usuario_id=payload.get('usuario_id', 0),
        data_necessaria=payload.get('data_necessaria'),
        observacao=payload.get('observacao')
    )

    # 4) chama o serviço
    service = PedidoService()
    try:
        out = service.create(dto)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 5) retorna JSON
    return JsonResponse({
        'id': out.id,
        'codigo': out.codigo,
        'usuario_id': out.usuario_id,
        'data_solicitacao': out.data_solicitacao.isoformat(),
        'status': out.status,
        'data_necessaria': out.data_necessaria.isoformat() if out.data_necessaria else None,
        'observacao': out.observacao,
    }, status=201)
