import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_cliente_service import CriarClienteService

@require_POST
def criar_cliente(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarClienteService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        cliente = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': cliente.id,
        'matricula': cliente.matricula,
        'nome_completo': cliente.nome_completo,
        'email': cliente.email,
        'telefone': cliente.telefone,
        'curso': cliente.curso
    }, status=201)
