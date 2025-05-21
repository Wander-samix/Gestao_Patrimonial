# interface/controllers/configuracao_estoque_controller.py

import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.contracts.configuracao_estoque_service_contract import IConfiguracaoEstoqueService
from core.application.services.criar_configuracao_estoque_service import ConfiguracaoEstoqueService
from core.application.dtos.configuracao_estoque_dto import (
    CreateConfiguracaoEstoqueDTO,
    ConfiguracaoEstoqueDTO,
)

@require_POST
def criar_configuracao_estoque(request):
    # 1) Parse do JSON e validação básica de payload via DTO de entrada
    try:
        payload = json.loads(request.body)
        dto_in = CreateConfiguracaoEstoqueDTO(**payload)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except TypeError as e:
        return JsonResponse({'error': f'Parâmetros inválidos: {e}'}, status=400)

    # 2) Chama o serviço via contrato
    service: IConfiguracaoEstoqueService = ConfiguracaoEstoqueService()
    try:
        dto_out: ConfiguracaoEstoqueDTO = service.create(dto_in)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorna diretamente o DTO de saída
    return JsonResponse(dto_out.__dict__, status=201)
