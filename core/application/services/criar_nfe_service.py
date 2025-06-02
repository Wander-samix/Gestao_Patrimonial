# core/application/services/nfe_service.py

from datetime import date
from typing import List, Optional
from decimal import Decimal

from core.application.dtos.nfe_dto import CreateNfeDTO, NfeDTO
from core.models import NFe


class NfeService:
    """
    Serviço de aplicação para NFe, usando diretamente o Django ORM.
    """

    @staticmethod
    def create(dto: CreateNfeDTO) -> NfeDTO:
        # 1) Validações dos campos do DTO
        numero = dto.numero.strip()
        if not numero:
            raise ValueError("O campo 'numero' é obrigatório e não pode ser vazio.")
        if len(numero) > 50:
            numero = numero[:50]

        if not isinstance(dto.data_emissao, date):
            raise ValueError("O campo 'data_emissao' deve ser um objeto date.")

        cnpj = dto.cnpj_fornecedor.strip()
        if not (cnpj.isdigit() and len(cnpj) == 14):
            raise ValueError("O campo 'cnpj_fornecedor' deve ter exatos 14 dígitos numéricos.")

        peso = dto.peso
        if not (isinstance(peso, (int, float, Decimal)) and peso >= 0):
            raise ValueError("O campo 'peso' deve ser numérico e maior ou igual a zero.")

        valor_total = dto.valor_total
        if not (isinstance(valor_total, (int, float, Decimal)) and valor_total >= 0):
            raise ValueError("O campo 'valor_total' deve ser numérico e maior ou igual a zero.")

        itens: Optional[List[int]] = dto.itens_vinculados_ids
        if itens is not None:
            if not isinstance(itens, list) or any(not isinstance(i, int) or i <= 0 for i in itens):
                raise ValueError("'itens_vinculados_ids' deve ser uma lista de IDs inteiros positivos.")

        area_id = dto.area_id
        if area_id is not None and (not isinstance(area_id, int) or area_id <= 0):
            raise ValueError("O campo 'area_id' deve ser um inteiro positivo, se informado.")

        # 2) Cria a NFe via ORM
        nfe_obj = NFe.objects.create(
            numero=numero,
            data_emissao=dto.data_emissao,
            cnpj_fornecedor=cnpj,
            peso=float(peso),
            valor_total=float(valor_total),
            area_id=area_id
        )

        # 3) Se houver itens vinculados, atualiza a relação M2M
        if itens:
            nfe_obj.itens_vinculados.set(itens)
        nfe_obj.save()

        # 4) Converte para NfeDTO e retorna
        return NfeDTO(
            id=nfe_obj.id,
            numero=nfe_obj.numero,
            data_emissao=nfe_obj.data_emissao,
            cnpj_fornecedor=nfe_obj.cnpj_fornecedor,
            peso=nfe_obj.peso,
            valor_total=nfe_obj.valor_total,
            itens_vinculados_ids=list(nfe_obj.itens_vinculados.values_list('id', flat=True)),
            area_id=nfe_obj.area_id
        )

    @staticmethod
    def get_by_id(id: int) -> Optional[NfeDTO]:
        try:
            m = NFe.objects.get(pk=id)
        except NFe.DoesNotExist:
            return None

        return NfeDTO(
            id=m.id,
            numero=m.numero,
            data_emissao=m.data_emissao,
            cnpj_fornecedor=m.cnpj_fornecedor,
            peso=m.peso,
            valor_total=m.valor_total,
            itens_vinculados_ids=list(m.itens_vinculados.values_list('id', flat=True)),
            area_id=m.area_id
        )

    @staticmethod
    def list_all() -> List[NfeDTO]:
        dtos: List[NfeDTO] = []
        for m in NFe.objects.all().order_by('-data_emissao', '-id'):
            dtos.append(NfeDTO(
                id=m.id,
                numero=m.numero,
                data_emissao=m.data_emissao,
                cnpj_fornecedor=m.cnpj_fornecedor,
                peso=m.peso,
                valor_total=m.valor_total,
                itens_vinculados_ids=list(m.itens_vinculados.values_list('id', flat=True)),
                area_id=m.area_id
            ))
        return dtos

    @staticmethod
    def delete(id: int) -> None:
        NFe.objects.filter(pk=id).delete()
