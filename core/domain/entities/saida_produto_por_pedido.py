from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SaidaProdutoPorPedido:
    id: Optional[int]
    produto_id: int
    pedido_id: int
    quantidade: int
    data_saida: datetime
