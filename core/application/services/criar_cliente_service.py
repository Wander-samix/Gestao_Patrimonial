# core/application/services/cliente_service.py
from typing import List
from core.application.contracts.cliente_service_contract import IClienteService
from core.application.dtos.cliente_dto import CreateClienteDTO, ClienteDTO
from core.domain.entities.cliente import Cliente
from core.domain.repositories.cliente_repository import IClienteRepository
from infrastructure.repositories.django_cliente_repository import DjangoClienteRepository

class ClienteService(IClienteService):
    def __init__(self, repo: IClienteRepository = None):
        self.repo: IClienteRepository = repo or DjangoClienteRepository()

    def create(self, dto: CreateClienteDTO) -> ClienteDTO:
        # validações
        if not dto.matricula.strip():
            raise ValueError("Matrícula é obrigatória.")
        if not dto.nome_completo.strip():
            raise ValueError("Nome completo é obrigatório.")
        if '@' not in dto.email or not dto.email.strip():
            raise ValueError("Email inválido.")
        if not dto.telefone.strip():
            raise ValueError("Telefone é obrigatório.")
        if not dto.curso.strip():
            raise ValueError("Curso é obrigatório.")

        # cria entidade de domínio
        entidade = Cliente(
            matricula=dto.matricula.strip()[:50],
            nome_completo=dto.nome_completo.strip()[:255],
            email=dto.email.strip(),
            telefone=dto.telefone.strip()[:15],
            curso=dto.curso.strip()[:255],
        )

        salvo = self.repo.save(entidade)
        return ClienteDTO(
            id=salvo.id,
            matricula=salvo.matricula,
            nome_completo=salvo.nome_completo,
            email=salvo.email,
            telefone=salvo.telefone,
            curso=salvo.curso,
        )

    def find_by_id(self, id: int) -> ClienteDTO:
        entidade = self.repo.find_by_id(id)
        if entidade is None:
            raise ValueError(f"Cliente com id {id} não encontrado.")
        return ClienteDTO(
            id=entidade.id,
            matricula=entidade.matricula,
            nome_completo=entidade.nome_completo,
            email=entidade.email,
            telefone=entidade.telefone,
            curso=entidade.curso,
        )

    def list_all(self) -> List[ClienteDTO]:
        entidades = self.repo.list_all()
        return [
            ClienteDTO(
                id=e.id,
                matricula=e.matricula,
                nome_completo=e.nome_completo,
                email=e.email,
                telefone=e.telefone,
                curso=e.curso,
            )
            for e in entidades
        ]
