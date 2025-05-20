from typing import Dict, Any, List, Optional
from core.domain.entities.usuario import Usuario
from core.domain.repositories.usuario_repository import IUsuarioRepository
from infrastructure.repositories.django_usuario_repository import DjangoUsuarioRepository

class CriarUsuarioService:
    def __init__(self, repo: IUsuarioRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoUsuarioRepository()

    def execute(self, dados: Dict[str, Any]) -> Usuario:
        """
        dados esperados:
          - username: str (obrigatório, max_length=150)
          - password: str (obrigatório)
          - email: str (opcional, formato válido)
          - first_name: str (opcional, max_length=30)
          - last_name: str (opcional, max_length=150)
          - matricula: str (opcional, max_length=20)
          - papel: str (opcional, choices=['admin','operador','tecnico'], default 'operador')
          - ativo: bool (opcional, default True)
          - areas_ids: List[int] (opcional)
          - groups_ids: List[int] (opcional)
          - user_permissions_ids: List[int] (opcional)
        """
        # username
        username = dados.get('username')
        if not username or not isinstance(username, str) or not username.strip():
            raise ValueError("O campo 'username' é obrigatório e não pode ser vazio.")
        username = username.strip()[:150]

        # password
        password = dados.get('password')
        if not password or not isinstance(password, str):
            raise ValueError("O campo 'password' é obrigatório e deve ser uma string.")
        
        # email (opcional)
        email = dados.get('email')
        if email is not None:
            if not isinstance(email, str) or '@' not in email:
                raise ValueError("'email' deve ser um endereço de e-mail válido.")
            email = email.strip()

        # first_name (opcional)
        first_name = dados.get('first_name', '')
        if not isinstance(first_name, str):
            raise ValueError("'first_name' deve ser uma string.")
        first_name = first_name.strip()[:30]

        # last_name (opcional)
        last_name = dados.get('last_name', '')
        if not isinstance(last_name, str):
            raise ValueError("'last_name' deve ser uma string.")
        last_name = last_name.strip()[:150]

        # matricula (opcional)
        matricula = dados.get('matricula')
        if matricula is not None:
            if not isinstance(matricula, str):
                raise ValueError("'matricula' deve ser uma string.")
            matricula = matricula.strip()[:20]

        # papel (opcional)
        papel = dados.get('papel', 'operador')
        if papel not in ('admin', 'operador', 'tecnico'):
            raise ValueError(f"'papel' inválido: deve ser 'admin', 'operador' ou 'tecnico'.")
        
        #
