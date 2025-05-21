from abc import ABC, abstractmethod
from core.application.dtos.produto_dto import CreateProdutoDTO, ProdutoDTO

class IProdutoService(ABC):
    @abstractmethod
    def create(self, dto: CreateProdutoDTO) -> ProdutoDTO:
        """
        Cria um Produto e retorna seus dados em um DTO.
        """
        ...
