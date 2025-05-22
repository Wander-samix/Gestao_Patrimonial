from core.application.contracts.usuario_service_contract import IUsuarioService
from core.application.dtos.usuario_dto import CreateUsuarioDTO, UsuarioDTO
from core.domain.entities.usuario import Usuario
from core.domain.repositories.usuario_repository import IUsuarioRepository
from infrastructure.repositories.django_usuario_repository import DjangoUsuarioRepository

class UsuarioService(IUsuarioService):
    def __init__(self, repo: IUsuarioRepository = None):
        # Usa o repositório Django por padrão se nenhum for fornecido
        self._repo = repo or DjangoUsuarioRepository()

    def create(self, dto: CreateUsuarioDTO) -> UsuarioDTO:
        # Validações do DTO (exemplo)
        if not dto.username.strip():
            raise ValueError("`username` não pode ser vazio.")
        if len(dto.password) < 6:
            raise ValueError("`password` deve ter pelo menos 6 caracteres.")
        
        # Constrói a entidade de domínio
        entidade = Usuario(
            username   = dto.username,
            password   = dto.password,
            email      = dto.email,
            first_name = dto.first_name,
            last_name  = dto.last_name,
            matricula  = dto.matricula,
            papel      = dto.papel,
            ativo      = dto.ativo,
            areas_ids           = dto.areas_ids,
            groups_ids          = dto.groups_ids,
            user_permissions_ids= dto.user_permissions_ids,
        )

        # Persiste via repositório
        salvo = self._repo.save(entidade)

        # Retorna o DTO de saída
        return UsuarioDTO(
            id       = salvo.id,
            username = salvo.username,
            email    = salvo.email,
            first_name = salvo.first_name,
            last_name  = salvo.last_name,
            matricula  = salvo.matricula,
            papel      = salvo.papel,
            ativo      = salvo.ativo,
            areas_ids           = [a.id for a in salvo.areas.all()],
            groups_ids          = [g.id for g in salvo.groups.all()],
            user_permissions_ids= [p.id for p in salvo.user_permissions.all()],
        )