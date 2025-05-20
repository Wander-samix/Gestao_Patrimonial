from dataclasses import dataclass
from typing import Optional

@dataclass
class ItemPedido:
    id: Optional[int]
    pedido_id: int
    produto_id: int
    quantidade: int
    liberado: Optional[int]
    observacao: str
    estoque_no_pedido: Optional[int]
