import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.dtos.log_acao_dto import CreateLogAcaoDTO
from core.application.services.criar_log_acao_service import LogAcaoService
from core.application.contracts.log_acao_service_contract import ILogAcaoService

@require_POST
def criar_log_acao(request):
    # 1) Parse do JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) Criação do DTO
    dto_in = CreateLogAcaoDTO(
        usuario_id=payload.get('usuario_id'),
        acao=payload.get('acao', ''),
        detalhes=payload.get('detalhes', ''),
        data_hora=payload.get('data_hora'),
        ip=payload.get('ip')
    )

    # 3) Chamada ao serviço
    service: ILogAcaoService = LogAcaoService()
    try:
        dto_out = service.create(dto_in)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 4) Formata datetime e retorna
    resp = {
        'id': dto_out.id,
        'usuario_id': dto_out.usuario_id,
        'acao': dto_out.acao,
        'detalhes': dto_out.detalhes,
        'data_hora': dto_out.data_hora.isoformat() if dto_out.data_hora else None,
        'ip': dto_out.ip,
    }
    return JsonResponse(resp, status=201)
