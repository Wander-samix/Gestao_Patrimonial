# core/application/services/fornecedor_service.py
from typing import List, Optional
from core.application.contracts.fornecedor_service_contract import IFornecedorService
from core.application.dtos.fornecedor_dto import CreateFornecedorDTO, FornecedorDTO
from core.domain.entities.fornecedor import Fornecedor
from core.domain.repositories.fornecedor_repository import IFornecedorRepository
from infrastructure.repositories.django_fornecedor_repository import DjangoFornecedorRepository

class FornecedorService(IFornecedorService):
    def __init__(self, repo: IFornecedorRepository = None):
        self.repo = repo or DjangoFornecedorRepository()

    def create(self, dto: CreateFornecedorDTO) -> FornecedorDTO:
        # --- validações de negócio ---
        nome = dto.nome.strip()
        if not nome:
            raise ValueError("O campo 'nome' é obrigatório e não pode ser vazio.")
        if len(nome) > 255:
            nome = nome[:255]

        cnpj = dto.cnpj.strip() if dto.cnpj else None
        if cnpj:
            if not cnpj.isdigit() or len(cnpj) != 14:
                raise ValueError("'cnpj' deve conter exatamente 14 dígitos numéricos.")

        endereco = dto.endereco.strip() if dto.endereco else ""
        telefone = dto.telefone.strip()[:15] if dto.telefone else None
        email = dto.email.strip() if dto.email else None
        if email and '@' not in email:
            raise ValueError("'email' deve ser um endereço de e-mail válido.")

        ativo = dto.ativo
        if not isinstance(ativo, bool):
            raise ValueError("'ativo' deve ser booleano.")

        # --- cria a entidade de domínio ---
        entidade = Fornecedor(
            nome=nome,
            cnpj=cnpj,
            endereco=endereco,
            telefone=telefone,
            email=email,
            ativo=ativo
        )

        # --- persiste via repositório ---
        salvo = self.repo.save(entidade)

        # --- monta e retorna DTO de saída ---
        return FornecedorDTO(
            id=salvo.id,
            nome=salvo.nome,
            cnpj=salvo.cnpj,
            endereco=salvo.endereco,
            telefone=salvo.telefone,
            email=salvo.email,
            ativo=salvo.ativo
        )

    def find_by_id(self, id: int) -> Optional[FornecedorDTO]:
        e = self.repo.find_by_id(id)
        if not e:
            return None
        return FornecedorDTO(
            id=e.id,
            nome=e.nome,
            cnpj=e.cnpj,
            endereco=e.endereco,
            telefone=e.telefone,
            email=e.email,
            ativo=e.ativo
        )

    def list_all(self) -> List[FornecedorDTO]:
        todos = self.repo.list_all()
        return [
            FornecedorDTO(
                id=e.id,
                nome=e.nome,
                cnpj=e.cnpj,
                endereco=e.endereco,
                telefone=e.telefone,
                email=e.email,
                ativo=e.ativo
            ) for e in todos
        ]
