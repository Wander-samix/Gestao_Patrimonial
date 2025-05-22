import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from core.application.dtos.session_log_dto import CreateSessionLogDTO
from core.application.services.criar_session_log_service import SessionLogService
from datetime import datetime, timedelta

@require_POST
def criar_session_log(request):
    # 1) Parse JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) Monta o DTO (precisa converter datas de string ISO para datetime)
    try:
        login_time = datetime.fromisoformat(payload['login_time'])
    except Exception:
        return JsonResponse({'error': "'login_time' inválido"}, status=400)

    logout_time = None
    if payload.get('logout_time'):
        try:
            logout_time = datetime.fromisoformat(payload['logout_time'])
        except Exception:
            return JsonResponse({'error': "'logout_time' inválido"}, status=400)

    duration = None
    if payload.get('duration'):
        try:
            # espera segundos ou ISO 8601? aqui tratamos como segundos
            duration = timedelta(seconds=float(payload['duration']))
        except Exception:
            return JsonResponse({'error': "'duration' inválido"}, status=400)

    dto = CreateSessionLogDTO(
        user_id     = payload.get('user_id', 0),
        session_key = payload.get('session_key', '').strip(),
        login_time  = login_time,
        logout_time = logout_time,
        duration    = duration,
        ip          = payload.get('ip'),
    )

    # 3) Executa o serviço
    service = SessionLogService()
    try:
        out = service.create(dto)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 4) Retorna JSON
    return JsonResponse({
        'id':           out.id,
        'user_id':      out.user_id,
        'session_key':  out.session_key,
        'login_time':   out.login_time,
        'logout_time':  out.logout_time,
        'duration':     out.duration,
        'ip':           out.ip,
    }, status=201)
