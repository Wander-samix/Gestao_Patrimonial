import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from datetime import datetime, date

from core.application.dtos.nfe_dto import CreateNfeDTO
from core.application.services.criar_nfe_service import NfeService

@require_POST
def criar_nfe(request):
    # 1) parse JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) transforma strings de data, se necessário
    data_raw = payload.get('data_emissao')
    if isinstance(data_raw, str):
        try:
            payload['data_emissao'] = date.fromisoformat(data_raw)
        except ValueError:
            return JsonResponse({'error': "Formato de 'data_emissao' inválido, use YYYY-MM-DD."}, status=400)

    # 3) monta o DTO
    dto = CreateNfeDTO(
        numero=payload.get('numero', ''),
        data_emissao=payload.get('data_emissao'),
        cnpj_fornecedor=payload.get('cnpj_fornecedor', ''),
        peso=payload.get('peso', 0),
        valor_total=payload.get('valor_total', 0),
        itens_vinculados_ids=payload.get('itens_vinculados_ids'),
        area_id=payload.get('area_id'),
    )

    # 4) chama serviço
    service = NfeService()
    try:
        out = service.create(dto)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 5) retorna JSON final
    return JsonResponse({
        'id': out.id,
        'numero': out.numero,
        'data_emissao': out.data_emissao.isoformat(),
        'cnpj_fornecedor': out.cnpj_fornecedor,
        'peso': out.peso,
        'valor_total': float(out.valor_total),
        'itens_vinculados_ids': out.itens_vinculados_ids,
        'area_id': out.area_id,
    }, status=201)
