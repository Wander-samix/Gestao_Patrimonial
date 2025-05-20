from dataclasses import dataclass
from typing import Optional

@dataclass
class SubItemPedido:
    id: Optional[int]
    pedido_id: int
    produto_id: int
    quantidade: int
    estoque_no_pedido: Optional[int]
