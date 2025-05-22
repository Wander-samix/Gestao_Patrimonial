import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.dtos.cliente_dto import (
    CreateClienteDTO,
    ClienteDTO
)
from core.application.contracts.cliente_service_contract import IClienteService
from core.application.services.criar_cliente_service import ClienteService

@require_POST
def criar_cliente(request):
    # 1) Parse do JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) Monta DTO de entrada
    try:
        dto_in = CreateClienteDTO(
            matricula=payload.get('matricula'),
            nome_completo=payload.get('nome_completo'),
            email=payload.get('email'),
            telefone=payload.get('telefone'),
            curso=payload.get('curso'),
        )
    except TypeError as e:
        # Se faltar algum campo obrigatório no DTO
        return JsonResponse({'error': f'Campo ausente ou formato inválido: {e}'}, status=400)

    # 3) Invoca serviço (pode trocar implementação via IClienteService)
    service: IClienteService = ClienteService()
    try:
        dto_out: ClienteDTO = service.create(dto_in)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 4) Retorna o DTO de saída diretamente
    return JsonResponse(dto_out.__dict__, status=201)
