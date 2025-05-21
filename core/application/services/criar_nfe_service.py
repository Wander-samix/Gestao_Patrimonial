from datetime import date
from typing import List, Optional
from decimal import Decimal

from core.application.contracts.nfe_service_contract import INfeService
from core.application.dtos.nfe_dto import CreateNfeDTO, NfeDTO
from core.domain.entities.nfe import Nfe
from core.domain.repositories.nfe_repository import INfeRepository
from infrastructure.repositories.django_nfe_repository import DjangoNfeRepository

class NfeService(INfeService):
    def __init__(self, repo: INfeRepository = None):
        self.repo = repo or DjangoNfeRepository()

    def create(self, dto: CreateNfeDTO) -> NfeDTO:
        # numero
        numero = dto.numero.strip()
        if not numero:
            raise ValueError("O campo 'numero' é obrigatório e não pode ser vazio.")
        numero = numero[:50]

        # data_emissao
        if not isinstance(dto.data_emissao, date):
            raise ValueError("O campo 'data_emissao' deve ser um objeto date.")

        # cnpj_fornecedor
        cnpj = dto.cnpj_fornecedor.strip()
        if not (cnpj.isdigit() and len(cnpj) == 14):
            raise ValueError("O campo 'cnpj_fornecedor' deve ter 14 dígitos numéricos.")

        # peso
        peso = dto.peso
        if not (isinstance(peso, (int, float)) and peso >= 0):
            raise ValueError("O campo 'peso' deve ser numérico >= 0.")

        # valor_total
        valor_total = dto.valor_total
        if not (isinstance(valor_total, (int, float, Decimal)) and valor_total >= 0):
            raise ValueError("O campo 'valor_total' deve ser numérico >= 0.")

        # itens_vinculados_ids
        itens: Optional[List[int]] = dto.itens_vinculados_ids
        if itens is not None:
            if not all(isinstance(i, int) and i > 0 for i in itens):
                raise ValueError("'itens_vinculados_ids' deve ser lista de IDs inteiros positivos.")

        # area_id
        area_id = dto.area_id
        if area_id is not None:
            if not (isinstance(area_id, int) and area_id > 0):
                raise ValueError("'area_id' deve ser inteiro positivo, se informado.")

        # monta a entidade e persiste
        nfe = Nfe(
            numero=numero,
            data_emissao=dto.data_emissao,
            cnpj_fornecedor=cnpj,
            peso=peso,
            valor_total=valor_total,
            area_id=area_id
        )
        criado = self.repo.save(nfe)

        # associa many-to-many, se houver
        if itens:
            criado.itens_vinculados.set(itens)

        return NfeDTO(
            id=criado.id,
            numero=criado.numero,
            data_emissao=criado.data_emissao,
            cnpj_fornecedor=criado.cnpj_fornecedor,
            peso=criado.peso,
            valor_total=criado.valor_total,
            itens_vinculados_ids=[p.id for p in criado.itens_vinculados.all()],
            area_id=criado.area_id,
        )
