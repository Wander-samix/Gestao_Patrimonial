from abc import ABC, abstractmethod
from core.application.dtos.usuario_dto import CreateUsuarioDTO, UsuarioDTO

class IUsuarioService(ABC):

    @abstractmethod
    def create(self, dto: CreateUsuarioDTO) -> UsuarioDTO:
        """
        Cria um usuário via DTO de entrada e retorna um DTO de saída.
        """
        ...
