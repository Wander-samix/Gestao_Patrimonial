from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MovimentacaoEstoque:
    id: Optional[int]
    tipo: str               # 'entrada' ou 'saida'
    data: datetime
    usuario_id: int
    quantidade: int
    produto_id: int
    nota_fiscal_id: Optional[int]
    cliente_id: Optional[int]
