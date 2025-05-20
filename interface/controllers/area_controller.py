import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from core.application.services.criar_area_service import CriarAreaService

@require_POST
def criar_area(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarAreaService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        area = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload mínimo
    return JsonResponse({'id': area.id, 'nome': area.nome}, status=201)
