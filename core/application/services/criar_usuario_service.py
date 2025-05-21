from core.application.contracts.usuario_service_contract import IUsuarioService
from core.application.dtos.usuario_dto import CreateUsuarioDTO, UsuarioDTO
from core.application.services.criar_usuario_service import CriarUsuarioService as RawService

class UsuarioService(IUsuarioService):
    def __init__(self, repo=None):
        # reaproveita seu serviço existente de criação
        self._raw = RawService(repo)

    def create(self, dto: CreateUsuarioDTO) -> UsuarioDTO:
        # converte o DTO em dict para passar ao serviço legado
        dados = {
            'username': dto.username,
            'password': dto.password,
            'email': dto.email,
            'first_name': dto.first_name,
            'last_name': dto.last_name,
            'matricula': dto.matricula,
            'papel': dto.papel,
            'ativo': dto.ativo,
            'areas_ids': dto.areas_ids,
            'groups_ids': dto.groups_ids,
            'user_permissions_ids': dto.user_permissions_ids,
        }
        usuario = self._raw.execute(dados)

        # monta e retorna o DTO de saída
        return UsuarioDTO(
            id=usuario.id,
            username=usuario.username,
            email=usuario.email,
            first_name=usuario.first_name,
            last_name=usuario.last_name,
            matricula=usuario.matricula,
            papel=usuario.papel,
            ativo=usuario.ativo,
            areas_ids=[a.id for a in usuario.areas.all()],
            groups_ids=[g.id for g in usuario.groups.all()],
            user_permissions_ids=[p.id for p in usuario.user_permissions.all()],
        )
