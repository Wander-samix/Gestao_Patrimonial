import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_configuracao_estoque_service import CriarConfiguracao_estoqueService

@require_POST
def criar_configuracao_estoque(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarConfiguracao_estoqueService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        cfg = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': cfg.id,
        'area_id': cfg.area_id,
        'estoque_minimo': cfg.estoque_minimo
    }, status=201)
