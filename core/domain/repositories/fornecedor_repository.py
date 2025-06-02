# core/domain/repositories/fornecedor_repository.py

from abc import ABC, abstractmethod
from typing import Optional, List
from core.domain.entities.fornecedor import Fornecedor  # nossa entidade de domínio


class IFornecedorRepository(ABC):
    @abstractmethod
    def save(self, obj: Fornecedor) -> Fornecedor:
        """
        Persiste um Fornecedor (cria ou atualiza).
        Retorna a entidade Fornecedor com o ID preenchido.
        """
        ...

    @abstractmethod
    def find_by_cnpj(self, cnpj: str) -> Optional[Fornecedor]:
        """
        Busca um Fornecedor por CNPJ.
        Retorna None se não achar.
        """
        ...

    @abstractmethod
    def list_all(self) -> List[Fornecedor]:
        """
        Retorna todos os Fornecedores como entidades de domínio.
        """
        ...

    @abstractmethod
    def delete(self, id: int) -> None:
        """
        Remove o Fornecedor com o ID dado.
        """
        ...
