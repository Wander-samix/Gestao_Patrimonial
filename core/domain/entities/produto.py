from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Produto:
    id: Optional[int]
    nfe_numero: Optional[str]
    codigo_barras: str
    descricao: str
    fornecedor_id: int
    area_id: Optional[int]
    lote: int
    validade: Optional[date]
    quantidade: int
    quantidade_inicial: int
    preco_unitario: float
    status: str
    criado_por_id: Optional[int]
    criado_em: datetime
