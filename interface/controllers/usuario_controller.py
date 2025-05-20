import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.application.services.criar_usuario_service import CriarUsuarioService

@require_POST
def criar_usuario(request):
    # 1) Parse do JSON
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    service = CriarUsuarioService()
    # 2) Execução do serviço com captura de erros de validação
    try:
        usuario = service.execute(dados)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 3) Retorno com 201 e payload explícito
    return JsonResponse({
        'id': usuario.id,
        'username': usuario.username,
        'email': usuario.email,
        'first_name': usuario.first_name,
        'last_name': usuario.last_name,
        'matricula': usuario.matricula,
        'papel': usuario.papel,
        'ativo': usuario.ativo,
        'areas_ids': usuario.areas_ids,
        'groups_ids': usuario.groups_ids,
        'user_permissions_ids': usuario.user_permissions_ids,
    }, status=201)
