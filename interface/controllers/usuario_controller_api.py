import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from core.application.dtos.usuario_dto import CreateUsuarioDTO
from core.application.services.criar_usuario_service import UsuarioService

@require_POST
def criar_usuario(request):
    # 1) parse do JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) monta o DTO de entrada
    dto = CreateUsuarioDTO(
        username            = payload.get('username', '').strip(),
        password            = payload.get('password', ''),
        email               = payload.get('email'),
        first_name          = payload.get('first_name'),
        last_name           = payload.get('last_name'),
        matricula           = payload.get('matricula'),
        papel               = payload.get('papel'),
        ativo               = payload.get('ativo', True),
        areas_ids           = payload.get('areas_ids'),
        groups_ids          = payload.get('groups_ids'),
        user_permissions_ids= payload.get('user_permissions_ids'),
    )

    # 3) chama o serviço
    service = UsuarioService()
    try:
        out = service.create(dto)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # 4) devolve o DTO convertido em JSON
    return JsonResponse({
        'id':                  out.id,
        'username':            out.username,
        'email':               out.email,
        'first_name':          out.first_name,
        'last_name':           out.last_name,
        'matricula':           out.matricula,
        'papel':               out.papel,
        'ativo':               out.ativo,
        'areas_ids':           out.areas_ids,
        'groups_ids':          out.groups_ids,
        'user_permissions_ids':out.user_permissions_ids,
    }, status=201)
