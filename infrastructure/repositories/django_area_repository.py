from typing import List, Optional
from core.domain.entities.area import Area
from core.domain.repositories.area_repository import IAreaRepository
from core.models import Area as AreaModel

class DjangoAreaRepository(IAreaRepository):
    def save(self, obj: Area) -> Area:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Retorna a entidade de domínio com o id gerado/atualizado.
        """
        if getattr(obj, 'id', None):
            model = AreaModel.objects.get(pk=obj.id)
            model.nome = obj.nome
            model.save(update_fields=['nome'])
        else:
            model = AreaModel.objects.create(nome=obj.nome)
        return Area(id=model.id, nome=model.nome)

    def find_by_id(self, id: int) -> Optional[Area]:
        """
        Busca por PK; retorna None se não existir.
        """
        try:
            m = AreaModel.objects.get(pk=id)
            return Area(id=m.id, nome=m.nome)
        except AreaModel.DoesNotExist:
            return None

    def list_all(self) -> List[Area]:
        """
        Retorna todas as áreas como entidades de domínio.
        """
        return [Area(id=m.id, nome=m.nome) for m in AreaModel.objects.all()]

    def delete(self, id: int) -> None:
        """
        Remove o registro com a PK informada.
        """
        AreaModel.objects.filter(pk=id).delete()
