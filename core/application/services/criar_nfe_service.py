from typing import Dict, Any, List, Optional
from datetime import date
from core.domain.entities.nfe import Nfe
from core.domain.repositories.nfe_repository import INfeRepository
from infrastructure.repositories.django_nfe_repository import DjangoNfeRepository

class CriarNfeService:
    def __init__(self, repo: INfeRepository = None):
        # injeta o repositório ou usa a implementação Django por padrão
        self.repo = repo or DjangoNfeRepository()

    def execute(self, dados: Dict[str, Any]) -> Nfe:
        """
        dados esperados:
          - numero: str (obrigatório, max_length=50)
          - data_emissao: date (obrigatório)
          - cnpj_fornecedor: str (obrigatório, 14 dígitos)
          - peso: float (obrigatório, >= 0)
          - valor_total: float (ou Decimal, obrigatório, >= 0)
          - itens_vinculados_ids: List[int] (opcional)
          - area_id: int (opcional, >0)
        Retorna a entidade Nfe recém-criada.
        """
        # valida numero
        numero = dados.get('numero')
        if not numero or not isinstance(numero, str) or not numero.strip():
            raise ValueError("O campo 'numero' é obrigatório e não pode ser vazio.")
        numero = numero.strip()[:50]

        # valida data_emissao
        data_emissao = dados.get('data_emissao')
        if not isinstance(data_emissao, date):
            raise ValueError("O campo 'data_emissao' é obrigatório e deve ser um objeto date.")

        # valida cnpj_fornecedor
        cnpj = dados.get('cnpj_fornecedor')
        if not cnpj or not isinstance(cnpj, str):
            raise ValueError("O campo 'cnpj_fornecedor' é obrigatório e deve ser uma string de 14 dígitos.")
        cnpj = cnpj.strip()
        if not (cnpj.isdigit() and len(cnpj) == 14):
            raise ValueError("'cnpj_fornecedor' deve conter exatamente 14 dígitos numéricos.")

        # valida peso
        peso = dados.get('peso')
        if not (isinstance(peso, (int, float)) and peso >= 0):
            raise ValueError("O campo 'peso' é obrigatório e deve ser numérico >= 0.")

        # valida valor_total
        valor_total = dados.get('valor_total')
        if not (isinstance(valor_total, (int, float)) and valor_total >= 0):
            raise ValueError("O campo 'valor_total' é obrigatório e deve ser numérico >= 0.")

        # valida itens_vinculados_ids (opcional)
        itens_ids: Optional[List[int]] = dados.get('itens_vinculados_ids')
        if itens_ids is not None:
            if not isinstance(itens_ids, list) or not all(isinstance(i, int) and i > 0 for i in itens_ids):
                raise ValueError("'itens_vinculados_ids' deve ser uma lista de IDs inteiros positivos.")

        # valida area_id (opcional)
        area_id: Optional[int] = dados.get('area_id')
        if area_id is not None:
            if not isinstance(area_id, int) or area_id < 1:
                raise ValueError("'area_id' deve ser um inteiro positivo, se informado.")

        # monta a entidade de domínio
        nfe = Nfe(
            numero=numero,
            data_emissao=data_emissao,
            cnpj_fornecedor=cnpj,
            peso=peso,
            valor_total=valor_total,
            itens_vinculados_ids=itens_ids,
            area_id=area_id
        )

        # persiste e retorna
        return self.repo.save(nfe)
