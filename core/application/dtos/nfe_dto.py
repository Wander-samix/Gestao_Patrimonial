from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class CreateNfeDTO:
    numero: str
    data_emissao: date
    cnpj_fornecedor: str
    peso: float
    valor_total: float
    itens_vinculados_ids: Optional[List[int]] = None
    area_id: Optional[int] = None

@dataclass
class NfeDTO:
    id: int
    numero: str
    data_emissao: date
    cnpj_fornecedor: str
    peso: float
    valor_total: float
    itens_vinculados_ids: List[int]
    area_id: Optional[int]
