from typing import List, Optional
from core.domain.entities.configuracao_estoque import ConfiguracaoEstoque
from core.domain.repositories.configuracao_estoque_repository import IConfiguracaoEstoqueRepository
from core.models import ConfiguracaoEstoque as ConfiguracaoEstoqueModel

class DjangoConfiguracaoEstoqueRepository(IConfiguracaoEstoqueRepository):
    def save(self, obj: ConfiguracaoEstoque) -> ConfiguracaoEstoque:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Retorna a entidade de domínio com o id gerado/atualizado.
        """
        if getattr(obj, 'id', None):
            model = ConfiguracaoEstoqueModel.objects.get(pk=obj.id)
            model.area_id = obj.area_id
            model.estoque_minimo = obj.estoque_minimo
            model.save(update_fields=['area', 'estoque_minimo'])
        else:
            model = ConfiguracaoEstoqueModel.objects.create(
                area_id=obj.area_id,
                estoque_minimo=obj.estoque_minimo
            )
        return ConfiguracaoEstoque(
            id=model.id,
            area_id=model.area_id,
            estoque_minimo=model.estoque_minimo
        )

    def find_by_id(self, id: int) -> Optional[ConfiguracaoEstoque]:
        """
        Busca por PK; retorna None se não existir.
        """
        try:
            m = ConfiguracaoEstoqueModel.objects.get(pk=id)
            return ConfiguracaoEstoque(
                id=m.id,
                area_id=m.area_id,
                estoque_minimo=m.estoque_minimo
            )
        except ConfiguracaoEstoqueModel.DoesNotExist:
            return None

    def list_all(self) -> List[ConfiguracaoEstoque]:
        """
        Retorna todas as configurações como entidades de domínio.
        """
        return [
            ConfiguracaoEstoque(
                id=m.id,
                area_id=m.area_id,
                estoque_minimo=m.estoque_minimo
            )
            for m in ConfiguracaoEstoqueModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove o registro com a PK informada.
        """
        ConfiguracaoEstoqueModel.objects.filter(pk=id).delete()
