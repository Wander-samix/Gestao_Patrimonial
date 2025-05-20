from typing import Dict, Any
from core.domain.entities.configuracao_estoque import Configuracao_estoque
from core.domain.repositories.configuracao_estoque_repository import IConfiguracao_estoqueRepository
from infrastructure.repositories.django_configuracao_estoque_repository import DjangoConfiguracao_estoqueRepository

class CriarConfiguracao_estoqueService:
    def __init__(self, repo: IConfiguracao_estoqueRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoConfiguracao_estoqueRepository()

    def execute(self, dados: Dict[str, Any]) -> Configuracao_estoque:
        """
        dados esperados:
          - area_id: int (opcional, positivo)
          - estoque_minimo: int (obrigatório, inteiro >= 0)
        Retorna a entidade Configuracao_estoque recém-criada ou atualizada.
        """
        # valida campo obrigatório
        estoque_minimo = dados.get('estoque_minimo')
        if estoque_minimo is None:
            raise ValueError("O campo 'estoque_minimo' é obrigatório.")
        if not isinstance(estoque_minimo, int) or estoque_minimo < 0:
            raise ValueError("'estoque_minimo' deve ser um inteiro não-negativo.")

        # valida foreign key opcional
        area_id = dados.get('area_id')
        if area_id is not None:
            if not isinstance(area_id, int) or area_id < 1:
                raise ValueError("'area_id' deve ser um inteiro positivo, se informado.")

        # monta a entidade de domínio
        cfg = Configuracao_estoque(
            area_id=area_id,
            estoque_minimo=estoque_minimo
        )
        # persiste e retorna
        return self.repo.save(cfg)
