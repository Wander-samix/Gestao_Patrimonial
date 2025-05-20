from typing import List, Optional
from core.domain.entities.usuario import Usuario as UsuarioEntity
from core.domain.repositories.usuario_repository import IUsuarioRepository
from core.models import Usuario as UsuarioModel

class DjangoUsuarioRepository(IUsuarioRepository):
    def save(self, obj: UsuarioEntity) -> UsuarioEntity:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo usuário.
        Gera hash de senha via set_password e sincroniza M2M de áreas, grupos e permissões.
        """
        if getattr(obj, 'id', None):
            m = UsuarioModel.objects.get(pk=obj.id)
            m.username = obj.username
            if obj.password:
                m.set_password(obj.password)
            m.email = obj.email
            m.first_name = obj.first_name
            m.last_name = obj.last_name
            m.matricula = obj.matricula
            m.papel = obj.papel
            m.ativo = obj.ativo
            m.save(update_fields=[
                'username', 'email', 'first_name', 'last_name',
                'matricula', 'papel', 'ativo'
            ])
        else:
            m = UsuarioModel(
                username=obj.username,
                email=obj.email,
                first_name=obj.first_name,
                last_name=obj.last_name,
                matricula=obj.matricula,
                papel=obj.papel,
                ativo=obj.ativo
            )
            m.set_password(obj.password)
            m.save()

        # sincroniza relações M2M
        if getattr(obj, 'areas_ids', None) is not None:
            m.areas.set(obj.areas_ids)
        if getattr(obj, 'groups_ids', None) is not None:
            m.groups.set(obj.groups_ids)
        if getattr(obj, 'user_permissions_ids', None) is not None:
            m.user_permissions.set(obj.user_permissions_ids)

        return UsuarioEntity(
            id=m.id,
            username=m.username,
            # não retornamos a senha em texto claro
            email=m.email,
            first_name=m.first_name,
            last_name=m.last_name,
            matricula=m.matricula,
            papel=m.papel,
            ativo=m.ativo,
            areas_ids=list(m.areas.values_list('id', flat=True)),
            groups_ids=list(m.groups.values_list('id', flat=True)),
            user_permissions_ids=list(m.user_permissions.values_list('id', flat=True))
        )

    def find_by_id(self, id: int) -> Optional[UsuarioEntity]:
        try:
            m = UsuarioModel.objects.get(pk=id)
            return UsuarioEntity(
                id=m.id,
                username=m.username,
                email=m.email,
                first_name=m.first_name,
                last_name=m.last_name,
                matricula=m.matricula,
                papel=m.papel,
                ativo=m.ativo,
                areas_ids=list(m.areas.values_list('id', flat=True)),
                groups_ids=list(m.groups.values_list('id', flat=True)),
                user_permissions_ids=list(m.user_permissions.values_list('id', flat=True))
            )
        except UsuarioModel.DoesNotExist:
            return None

    def list_all(self) -> List[UsuarioEntity]:
        return [
            UsuarioEntity(
                id=m.id,
                username=m.username,
                email=m.email,
                first_name=m.first_name,
                last_name=m.last_name,
                matricula=m.matricula,
                papel=m.papel,
                ativo=m.ativo,
                areas_ids=list(m.areas.values_list('id', flat=True)),
                groups_ids=list(m.groups.values_list('id', flat=True)),
                user_permissions_ids=list(m.user_permissions.values_list('id', flat=True))
            )
            for m in UsuarioModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        UsuarioModel.objects.filter(pk=id).delete()
