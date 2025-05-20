from typing import Dict, Any
from core.domain.entities.cliente import Cliente
from core.domain.repositories.cliente_repository import IClienteRepository
from infrastructure.repositories.django_cliente_repository import DjangoClienteRepository

class CriarClienteService:
    def __init__(self, repo: IClienteRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoClienteRepository()

    def execute(self, dados: Dict[str, Any]) -> Cliente:
        """
        dados esperados:
          - matricula: str (obrigatório, max_length=50)
          - nome_completo: str (obrigatório, max_length=255)
          - email: str (obrigatório, formato básico)
          - telefone: str (obrigatório, max_length=15)
          - curso: str (obrigatório, max_length=255)
        Retorna a entidade Cliente recém-criada.
        """
        # valida matricula
        matricula = dados.get('matricula')
        if not matricula or not isinstance(matricula, str) or not matricula.strip():
            raise ValueError("O campo 'matricula' é obrigatório e não pode ser vazio.")
        matricula = matricula.strip()[:50]

        # valida nome_completo
        nome = dados.get('nome_completo')
        if not nome or not isinstance(nome, str) or not nome.strip():
            raise ValueError("O campo 'nome_completo' é obrigatório e não pode ser vazio.")
        nome = nome.strip()[:255]

        # valida email (cheque básico)
        email = dados.get('email')
        if not email or not isinstance(email, str) or '@' not in email:
            raise ValueError("O campo 'email' é obrigatório e deve ser um endereço válido.")
        email = email.strip()

        # valida telefone
        telefone = dados.get('telefone')
        if not telefone or not isinstance(telefone, str) or not telefone.strip():
            raise ValueError("O campo 'telefone' é obrigatório e não pode ser vazio.")
        telefone = telefone.strip()[:15]

        # valida curso
        curso = dados.get('curso')
        if not curso or not isinstance(curso, str) or not curso.strip():
            raise ValueError("O campo 'curso' é obrigatório e não pode ser vazio.")
        curso = curso.strip()[:255]

        # monta a entidade de domínio
        cliente = Cliente(
            matricula=matricula,
            nome_completo=nome,
            email=email,
            telefone=telefone,
            curso=curso
        )
        # persiste e retorna
        return self.repo.save(cliente)
