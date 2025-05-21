# interface/controllers/fornecedor_controller.py

import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.contracts.fornecedor_service_contract import IFornecedorService
from core.application.services.criar_fornecedor_service import FornecedorService
from core.application.dtos.fornecedor_dto import CreateFornecedorDTO

@require_POST
def criar_fornecedor(request):
    # 1) Parse do JSON
    try:
        payload = json.loads(request.body)
        dto = CreateFornecedorDTO(**payload)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except TypeError as e:
        # campos faltando ou extras
        return JsonResponse({'error': f'Parâmetros inválidos: {e}'}, status=400)

    # 2) Execução do serviço com captura de erro de negócio
    service: IFornecedorService = FornecedorService()
    try:
        out_dto = service.create(dto)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload proveniente do DTO de saída
    return JsonResponse(out_dto.__dict__, status=201)
