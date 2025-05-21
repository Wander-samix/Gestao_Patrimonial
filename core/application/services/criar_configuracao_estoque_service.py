from core.application.contracts.configuracao_estoque_service_contract import IConfiguracaoEstoqueService
from core.application.dtos.configuracao_estoque_dto import (
    CreateConfiguracaoEstoqueDTO,
    ConfiguracaoEstoqueDTO,
)
from core.domain.entities.configuracao_estoque import ConfiguracaoEstoque
from core.domain.repositories.configuracao_estoque_repository import IConfiguracaoEstoqueRepository
from infrastructure.repositories.django_configuracao_estoque_repository import DjangoConfiguracaoEstoqueRepository

class ConfiguracaoEstoqueService(IConfiguracaoEstoqueService):
    def __init__(self, repo: IConfiguracaoEstoqueRepository = None):
        self.repo = repo or DjangoConfiguracaoEstoqueRepository()

    def create(self, dto: CreateConfiguracaoEstoqueDTO) -> ConfiguracaoEstoqueDTO:
        # Validações de regra de negócio
        if dto.estoque_minimo is None:
            raise ValueError("O campo 'estoque_minimo' é obrigatório.")
        if dto.estoque_minimo < 0:
            raise ValueError("'estoque_minimo' deve ser um inteiro não-negativo.")

        if dto.area_id is not None and dto.area_id < 1:
            raise ValueError("'area_id' deve ser um inteiro positivo, se informado.")

        # Monta a entidade de domínio
        entidade = ConfiguracaoEstoque(
            area_id=dto.area_id,
            estoque_minimo=dto.estoque_minimo,
        )

        # Persiste e monta DTO de saída
        salvo = self.repo.save(entidade)
        return ConfiguracaoEstoqueDTO(
            id=salvo.id,
            area_id=salvo.area_id,
            estoque_minimo=salvo.estoque_minimo,
        )
