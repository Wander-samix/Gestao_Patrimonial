from typing import List, Optional
from core.domain.entities.nfe import Nfe
from core.domain.repositories.nfe_repository import INfeRepository
from core.models import NFe as NFeModel

class DjangoNfeRepository(INfeRepository):
    def save(self, obj: Nfe) -> Nfe:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Também ajusta o relacionamento M2M de itens_vinculados.
        """
        if getattr(obj, 'id', None):
            m = NFeModel.objects.get(pk=obj.id)
            m.numero = obj.numero
            m.data_emissao = obj.data_emissao
            m.cnpj_fornecedor = obj.cnpj_fornecedor
            m.peso = obj.peso
            m.valor_total = obj.valor_total
            m.area_id = obj.area_id
            m.save(update_fields=[
                'numero', 'data_emissao', 'cnpj_fornecedor',
                'peso', 'valor_total', 'area'
            ])
        else:
            m = NFeModel.objects.create(
                numero=obj.numero,
                data_emissao=obj.data_emissao,
                cnpj_fornecedor=obj.cnpj_fornecedor,
                peso=obj.peso,
                valor_total=obj.valor_total,
                area_id=obj.area_id
            )

        # sincroniza itens vinculados, se houver IDs
        if getattr(obj, 'itens_vinculados_ids', None) is not None:
            m.itens_vinculados.set(obj.itens_vinculados_ids)

        return Nfe(
            id=m.id,
            numero=m.numero,
            data_emissao=m.data_emissao,
            cnpj_fornecedor=m.cnpj_fornecedor,
            peso=m.peso,
            valor_total=m.valor_total,
            itens_vinculados_ids=list(m.itens_vinculados.values_list('id', flat=True)),
            area_id=m.area_id
        )

    def find_by_id(self, id: int) -> Optional[Nfe]:
        """
        Busca NFe por PK; retorna None se não existir.
        """
        try:
            m = NFeModel.objects.get(pk=id)
            return Nfe(
                id=m.id,
                numero=m.numero,
                data_emissao=m.data_emissao,
                cnpj_fornecedor=m.cnpj_fornecedor,
                peso=m.peso,
                valor_total=m.valor_total,
                itens_vinculados_ids=list(m.itens_vinculados.values_list('id', flat=True)),
                area_id=m.area_id
            )
        except NFeModel.DoesNotExist:
            return None

    def list_all(self) -> List[Nfe]:
        """
        Retorna todas as NFe como entidades de domínio.
        """
        result: List[Nfe] = []
        for m in NFeModel.objects.all():
            result.append(Nfe(
                id=m.id,
                numero=m.numero,
                data_emissao=m.data_emissao,
                cnpj_fornecedor=m.cnpj_fornecedor,
                peso=m.peso,
                valor_total=m.valor_total,
                itens_vinculados_ids=list(m.itens_vinculados.values_list('id', flat=True)),
                area_id=m.area_id
            ))
        return result

    def delete(self, id: int) -> None:
        """
        Remove a NFe com a PK informada.
        """
        NFeModel.objects.filter(pk=id).delete()
