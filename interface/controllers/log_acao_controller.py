import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_log_acao_service import CriarLog_acaoService

@require_POST
def criar_log_acao(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarLog_acaoService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        log = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': log.id,
        'usuario_id': log.usuario_id,
        'acao': log.acao,
        'detalhes': log.detalhes,
        'data_hora': log.data_hora.isoformat(),
        'ip': log.ip,
    }, status=201)
