from typing import Dict, Any
from core.domain.entities.area import Area
from core.domain.repositories.area_repository import IAreaRepository
from infrastructure.repositories.django_area_repository import DjangoAreaRepository

class CriarAreaService:
    def __init__(self, repo: IAreaRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoAreaRepository()

    def execute(self, dados: Dict[str, Any]) -> Area:
        """
        dados esperado:
          - nome: str (obrigatório, max_length=100)
        Retorna a entidade Area recém-criada.
        """
        nome = dados.get('nome')
        if not nome or not isinstance(nome, str) or not nome.strip():
            raise ValueError("O campo 'nome' é obrigatório e não pode ser vazio.")
        
        nome = nome.strip()
        # aplica o mesmo limite de 100 caracteres do CharField
        if len(nome) > 100:
            nome = nome[:100]

        # cria a entidade de domínio e persiste via repositório
        area = Area(nome=nome)
        return self.repo.save(area)
