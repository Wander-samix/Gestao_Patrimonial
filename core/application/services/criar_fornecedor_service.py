from typing import Dict, Any
from core.domain.entities.fornecedor import Fornecedor
from core.domain.repositories.fornecedor_repository import IFornecedorRepository
from infrastructure.repositories.django_fornecedor_repository import DjangoFornecedorRepository

class CriarFornecedorService:
    def __init__(self, repo: IFornecedorRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoFornecedorRepository()

    def execute(self, dados: Dict[str, Any]) -> Fornecedor:
        """
        dados esperados:
          - nome: str (obrigatório, max_length=255)
          - cnpj: str (opcional, 14 dígitos)
          - endereco: str (opcional)
          - telefone: str (opcional, max_length=15)
          - email: str (opcional, formato válido)
          - ativo: bool (opcional, default True)
        Retorna a entidade Fornecedor recém-criada.
        """
        # nome (obrigatório)
        nome = dados.get('nome')
        if not nome or not isinstance(nome, str) or not nome.strip():
            raise ValueError("O campo 'nome' é obrigatório e não pode ser vazio.")
        nome = nome.strip()[:255]

        # cnpj (opcional)
        cnpj = dados.get('cnpj')
        if cnpj is not None:
            if not isinstance(cnpj, str):
                raise ValueError("'cnpj' deve ser uma string de 14 dígitos.")
            cnpj = cnpj.strip()
            if cnpj and (not cnpj.isdigit() or len(cnpj) != 14):
                raise ValueError("'cnpj' deve conter exatamente 14 dígitos numéricos.")

        # endereco (opcional)
        endereco = dados.get('endereco')
        if endereco is None:
            endereco = ''
        elif not isinstance(endereco, str):
            raise ValueError("'endereco' deve ser uma string.")
        else:
            endereco = endereco.strip()

        # telefone (opcional)
        telefone = dados.get('telefone')
        if telefone is not None:
            if not isinstance(telefone, str) or not telefone.strip():
                raise ValueError("'telefone' deve ser uma string não vazia.")
            telefone = telefone.strip()[:15]

        # email (opcional)
        email = dados.get('email')
        if email is not None:
            if not isinstance(email, str) or '@' not in email:
                raise ValueError("'email' deve ser um endereço de e-mail válido.")
            email = email.strip()

        # ativo (opcional)
        ativo = dados.get('ativo', True)
        if not isinstance(ativo, bool):
            raise ValueError("'ativo' deve ser um booleano.")

        # monta a entidade de domínio
        fornecedor = Fornecedor(
            nome=nome,
            cnpj=cnpj,
            endereco=endereco,
            telefone=telefone,
            email=email,
            ativo=ativo
        )
        # persiste e retorna
        return self.repo.save(fornecedor)
