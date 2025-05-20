from typing import List, Optional
from core.domain.entities.fornecedor import Fornecedor
from core.domain.repositories.fornecedor_repository import IFornecedorRepository
from core.models import Fornecedor as FornecedorModel

class DjangoFornecedorRepository(IFornecedorRepository):
    def save(self, obj: Fornecedor) -> Fornecedor:
        """
        Se obj.id existir, atualiza; caso contrário, cria novo registro.
        Retorna a entidade de domínio com o id gerado/atualizado.
        """
        if getattr(obj, 'id', None):
            model = FornecedorModel.objects.get(pk=obj.id)
            model.nome     = obj.nome
            model.cnpj     = obj.cnpj
            model.endereco = obj.endereco
            model.telefone = obj.telefone
            model.email    = obj.email
            model.ativo    = obj.ativo
            model.save(update_fields=['nome', 'cnpj', 'endereco', 'telefone', 'email', 'ativo'])
        else:
            model = FornecedorModel.objects.create(
                nome=obj.nome,
                cnpj=obj.cnpj,
                endereco=obj.endereco,
                telefone=obj.telefone,
                email=obj.email,
                ativo=obj.ativo
            )
        return Fornecedor(
            id=model.id,
            nome=model.nome,
            cnpj=model.cnpj,
            endereco=model.endereco,
            telefone=model.telefone,
            email=model.email,
            ativo=model.ativo
        )

    def find_by_id(self, id: int) -> Optional[Fornecedor]:
        """
        Busca Fornecedor por PK; retorna None se não existir.
        """
        try:
            m = FornecedorModel.objects.get(pk=id)
            return Fornecedor(
                id=m.id,
                nome=m.nome,
                cnpj=m.cnpj,
                endereco=m.endereco,
                telefone=m.telefone,
                email=m.email,
                ativo=m.ativo
            )
        except FornecedorModel.DoesNotExist:
            return None

    def list_all(self) -> List[Fornecedor]:
        """
        Retorna todos os Fornecedores como entidades de domínio.
        """
        return [
            Fornecedor(
                id=m.id,
                nome=m.nome,
                cnpj=m.cnpj,
                endereco=m.endereco,
                telefone=m.telefone,
                email=m.email,
                ativo=m.ativo
            )
            for m in FornecedorModel.objects.all()
        ]

    def delete(self, id: int) -> None:
        """
        Remove o Fornecedor com a PK informada.
        """
        FornecedorModel.objects.filter(pk=id).delete()
