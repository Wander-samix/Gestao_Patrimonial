import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.dtos.area_dto import CreateAreaDTO, AreaDTO
from core.application.contracts.area_service_contract import IAreaService
from core.application.services.criar_area_service import CriarAreaService

@require_POST
def criar_area(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) DTO de entrada
    try:
        dto_in = CreateAreaDTO(nome=payload['nome'])
    except KeyError:
        return JsonResponse({'error': "O campo 'nome' é obrigatório"}, status=400)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) chama via contrato
    service: IAreaService = CriarAreaService()
    try:
        dto_out: AreaDTO = service.create(dto_in)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 4) monta resposta
    return JsonResponse({'id': dto_out.id, 'nome': dto_out.nome}, status=201)
