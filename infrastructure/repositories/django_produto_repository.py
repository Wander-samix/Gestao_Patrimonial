from datetime import date, timedelta
from typing import List, Optional
from django.db.models import Q

from core.domain.entities.produto import Produto
from core.domain.repositories.produto_repository import IProdutoRepository
from core.models import Produto as ProdutoModel


class DjangoProdutoRepository(IProdutoRepository):
    def save(self, obj: Produto) -> Produto:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Note que lote e quantidade_inicial são gerenciados pelo model.
        Retorna a entidade de domínio com o id e demais campos preenchidos.
        """
        if getattr(obj, 'id', None):
            m = ProdutoModel.objects.get(pk=obj.id)
            m.nfe_numero      = obj.nfe_numero
            m.codigo_barras   = obj.codigo_barras
            m.descricao       = obj.descricao
            m.fornecedor_id   = obj.fornecedor_id
            m.area_id         = obj.area_id
            m.validade        = obj.validade
            m.quantidade      = obj.quantidade
            m.preco_unitario  = obj.preco_unitario
            m.save(update_fields=[
                'nfe_numero', 'codigo_barras', 'descricao',
                'fornecedor', 'area', 'validade',
                'quantidade', 'preco_unitario'
            ])
        else:
            m = ProdutoModel.objects.create(
                nfe_numero     = obj.nfe_numero,
                codigo_barras  = obj.codigo_barras,
                descricao      = obj.descricao,
                fornecedor_id  = obj.fornecedor_id,
                area_id        = obj.area_id,
                validade       = obj.validade,
                quantidade     = obj.quantidade,
                preco_unitario = obj.preco_unitario
            )

        return Produto(
            id                  = m.id,
            nfe_numero          = m.nfe_numero,
            codigo_barras       = m.codigo_barras,
            descricao           = m.descricao,
            fornecedor_id       = m.fornecedor_id,
            area_id             = m.area_id,
            lote                = m.lote,
            validade            = m.validade,
            quantidade          = m.quantidade,
            quantidade_inicial  = m.quantidade_inicial,
            preco_unitario      = m.preco_unitario,
            status              = m.status,
            criado_por_id       = m.criado_por_id,
            criado_em           = m.criado_em
        )

    def find_by_id(self, id: int) -> Optional[Produto]:
        """
        Busca Produto por PK; retorna None se não existir.
        """
        try:
            m = ProdutoModel.objects.get(pk=id)
            return Produto(
                id                  = m.id,
                nfe_numero          = m.nfe_numero,
                codigo_barras       = m.codigo_barras,
                descricao           = m.descricao,
                fornecedor_id       = m.fornecedor_id,
                area_id             = m.area_id,
                lote                = m.lote,
                validade            = m.validade,
                quantidade          = m.quantidade,
                quantidade_inicial  = m.quantidade_inicial,
                preco_unitario      = m.preco_unitario,
                status              = m.status,
                criado_por_id       = m.criado_por_id,
                criado_em           = m.criado_em
            )
        except ProdutoModel.DoesNotExist:
            return None

    def list_all(self) -> List[Produto]:
        """
        Retorna todos os Produtos como entidades de domínio.
        """
        return [
            Produto(
                id                  = m.id,
                nfe_numero          = m.nfe_numero,
                codigo_barras       = m.codigo_barras,
                descricao           = m.descricao,
                fornecedor_id       = m.fornecedor_id,
                area_id             = m.area_id,
                lote                = m.lote,
                validade            = m.validade,
                quantidade          = m.quantidade,
                quantidade_inicial  = m.quantidade_inicial,
                preco_unitario      = m.preco_unitario,
                status              = m.status,
                criado_por_id       = m.criado_por_id,
                criado_em           = m.criado_em
            )
            for m in ProdutoModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove o Produto com a PK informada.
        """
        ProdutoModel.objects.filter(pk=id).delete()

    def listar_filtrado(
        self,
        busca: Optional[str] = None,
        area_id: Optional[int] = None,
        status: Optional[str] = None,
        validade: Optional[str] = None  # None | 'vencido' | 'proximo'
    ) -> List[Produto]:
        """
        Filtra produtos por busca, área, status e validade (vencido/próximo).
        """
        qs = ProdutoModel.objects.all()
        hoje = date.today()

        if busca:
            qs = qs.filter(
                Q(descricao__icontains=busca) | Q(codigo_barras__icontains=busca)
            )
        if area_id:
            qs = qs.filter(area_id=area_id)
        if status:
            qs = qs.filter(status=status)

        if validade == 'vencido':
            qs = qs.filter(validade__lt=hoje)
        elif validade == 'proximo':
            qs = qs.filter(validade__gte=hoje, validade__lte=hoje + timedelta(days=7))

        # Opcional: ordenação
        qs = qs.order_by('validade', 'descricao')

        return [
            Produto(
                id                  = m.id,
                nfe_numero          = m.nfe_numero,
                codigo_barras       = m.codigo_barras,
                descricao           = m.descricao,
                fornecedor_id       = m.fornecedor_id,
                area_id             = m.area_id,
                lote                = m.lote,
                validade            = m.validade,
                quantidade          = m.quantidade,
                quantidade_inicial  = m.quantidade_inicial,
                preco_unitario      = m.preco_unitario,
                status              = m.status,
                criado_por_id       = m.criado_por_id,
                criado_em           = m.criado_em
            )
            for m in qs
        ]