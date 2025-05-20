from typing import List, Optional
from core.domain.entities.cliente import Cliente
from core.domain.repositories.cliente_repository import IClienteRepository
from core.models import Cliente as ClienteModel

class DjangoClienteRepository(IClienteRepository):
    def save(self, obj: Cliente) -> Cliente:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        """
        if getattr(obj, 'id', None):
            model = ClienteModel.objects.get(pk=obj.id)
            model.matricula    = obj.matricula
            model.nome_completo = obj.nome_completo
            model.email        = obj.email
            model.telefone     = obj.telefone
            model.curso        = obj.curso
            model.save(update_fields=['matricula', 'nome_completo', 'email', 'telefone', 'curso'])
        else:
            model = ClienteModel.objects.create(
                matricula=obj.matricula,
                nome_completo=obj.nome_completo,
                email=obj.email,
                telefone=obj.telefone,
                curso=obj.curso
            )
        return Cliente(
            id=model.id,
            matricula=model.matricula,
            nome_completo=model.nome_completo,
            email=model.email,
            telefone=model.telefone,
            curso=model.curso
        )

    def find_by_id(self, id: int) -> Optional[Cliente]:
        """
        Busca Cliente por PK; retorna None se não existir.
        """
        try:
            m = ClienteModel.objects.get(pk=id)
            return Cliente(
                id=m.id,
                matricula=m.matricula,
                nome_completo=m.nome_completo,
                email=m.email,
                telefone=m.telefone,
                curso=m.curso
            )
        except ClienteModel.DoesNotExist:
            return None

    def list_all(self) -> List[Cliente]:
        """
        Retorna todas as Clientes como entidades de domínio.
        """
        return [
            Cliente(
                id=m.id,
                matricula=m.matricula,
                nome_completo=m.nome_completo,
                email=m.email,
                telefone=m.telefone,
                curso=m.curso
            )
            for m in ClienteModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove o Cliente com a PK informada.
        """
        ClienteModel.objects.filter(pk=id).delete()
