from typing import List, Optional
from core.domain.entities.movimentacao_estoque import MovimentacaoEstoque
from core.domain.repositories.movimentacao_estoque_repository import IMovimentacaoEstoqueRepository
from core.models import MovimentacaoEstoque as MovimentacaoEstoqueModel

class DjangoMovimentacaoEstoqueRepository(IMovimentacaoEstoqueRepository):
    def save(self, obj: MovimentacaoEstoque) -> MovimentacaoEstoque:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Retorna a entidade de domínio com o id gerado/atualizado.
        """
        if getattr(obj, 'id', None):
            m = MovimentacaoEstoqueModel.objects.get(pk=obj.id)
            m.tipo           = obj.tipo
            m.data           = obj.data
            m.usuario_id     = obj.usuario_id
            m.quantidade     = obj.quantidade
            m.produto_id     = obj.produto_id
            m.nota_fiscal_id = obj.nota_fiscal_id
            m.cliente_id     = obj.cliente_id
            m.save(update_fields=[
                'tipo', 'data', 'usuario', 'quantidade',
                'produto', 'nota_fiscal', 'cliente'
            ])
        else:
            m = MovimentacaoEstoqueModel.objects.create(
                tipo=obj.tipo,
                data=obj.data,
                usuario_id=obj.usuario_id,
                quantidade=obj.quantidade,
                produto_id=obj.produto_id,
                nota_fiscal_id=obj.nota_fiscal_id,
                cliente_id=obj.cliente_id
            )
        return MovimentacaoEstoque(
            id=m.id,
            tipo=m.tipo,
            data=m.data,
            usuario_id=m.usuario_id,
            quantidade=m.quantidade,
            produto_id=m.produto_id,
            nota_fiscal_id=m.nota_fiscal_id,
            cliente_id=m.cliente_id
        )

    def find_by_id(self, id: int) -> Optional[MovimentacaoEstoque]:
        """
        Busca MovimentacaoEstoque por PK; retorna None se não existir.
        """
        try:
            m = MovimentacaoEstoqueModel.objects.get(pk=id)
            return MovimentacaoEstoque(
                id=m.id,
                tipo=m.tipo,
                data=m.data,
                usuario_id=m.usuario_id,
                quantidade=m.quantidade,
                produto_id=m.produto_id,
                nota_fiscal_id=m.nota_fiscal_id,
                cliente_id=m.cliente_id
            )
        except MovimentacaoEstoqueModel.DoesNotExist:
            return None

    def list_all(self) -> List[MovimentacaoEstoque]:
        """
        Retorna todas as movimentações de estoque como entidades de domínio.
        """
        return [
            MovimentacaoEstoque(
                id=m.id,
                tipo=m.tipo,
                data=m.data,
                usuario_id=m.usuario_id,
                quantidade=m.quantidade,
                produto_id=m.produto_id,
                nota_fiscal_id=m.nota_fiscal_id,
                cliente_id=m.cliente_id
            )
            for m in MovimentacaoEstoqueModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove a movimentação de estoque com a PK informada.
        """
        MovimentacaoEstoqueModel.objects.filter(pk=id).delete()
