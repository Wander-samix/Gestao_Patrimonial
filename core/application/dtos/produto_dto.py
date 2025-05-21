from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

@dataclass
class CreateProdutoDTO:
    codigo_barras: str
    descricao: str
    fornecedor_id: int
    quantidade: int
    preco_unitario: Decimal = Decimal("0")
    nfe_numero: Optional[str] = None
    area_id: Optional[int] = None
    validade: Optional[date] = None

@dataclass
class ProdutoDTO:
    id: int
    codigo_barras: str
    descricao: str
    fornecedor_id: int
    quantidade: int
    preco_unitario: Decimal
    nfe_numero: Optional[str]
    area_id: Optional[int]
    validade: Optional[date]
    lote: int
    criado_em: date
