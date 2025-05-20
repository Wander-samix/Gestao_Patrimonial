from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class NFe:
    id: Optional[int]
    numero: str
    data_emissao: date
    cnpj_fornecedor: str
    peso: float
    valor_total: float
    itens_vinculados_ids: List[int]  # IDs de Produto
    area_id: Optional[int]
