import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_session_log_service import CriarSession_logService

@require_POST
def criar_session_log(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarSession_logService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        sess = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': sess.id,
        'user_id': sess.user_id,
        'session_key': sess.session_key,
        'login_time': sess.login_time.isoformat(),
        'logout_time': sess.logout_time.isoformat() if sess.logout_time else None,
        'duration_seconds': sess.duration.total_seconds() if sess.duration else None,
        'ip': sess.ip,
    }, status=201)
