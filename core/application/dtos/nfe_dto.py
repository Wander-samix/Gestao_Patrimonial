# core/domain/dtos/nfe_dto.py

from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class CreateNfeDTO:
    """
    DTO usado para criação de uma nova NFe. 
    Contém apenas os campos obrigatórios na criação.
    """
    numero: str
    data_emissao: date
    cnpj_fornecedor: str
    peso: float
    valor_total: float
    itens_vinculados_ids: Optional[List[int]] = None
    area_id: Optional[int] = None


@dataclass
class NfeDTO:
    """
    DTO usado para transferência (return) de uma NFe já salva.
    Contém o ID e todos os campos.
    """
    id: int
    numero: str
    data_emissao: date
    cnpj_fornecedor: str
    peso: float
    valor_total: float
    itens_vinculados_ids: List[int]
    area_id: Optional[int]
