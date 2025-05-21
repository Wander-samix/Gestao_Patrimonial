from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CreateMovimentacaoEstoqueDTO:
    tipo: str
    data: Optional[datetime] = None
    usuario_id: int = 0
    quantidade: int = 0
    produto_id: int = 0
    nota_fiscal_id: Optional[int] = None
    cliente_id: Optional[int] = None

@dataclass
class MovimentacaoEstoqueDTO:
    id: int
    tipo: str
    data: datetime
    usuario_id: int
    quantidade: int
    produto_id: int
    nota_fiscal_id: Optional[int]
    cliente_id: Optional[int]
