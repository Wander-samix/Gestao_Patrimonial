from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateItemPedidoDTO:
    pedido_id: int
    produto_id: int
    quantidade: int
    liberado: Optional[int] = None
    observacao: str = ''
    estoque_no_pedido: Optional[int] = None

@dataclass
class ItemPedidoDTO:
    id: int
    pedido_id: int
    produto_id: int
    quantidade: int
    liberado: Optional[int]
    observacao: str
    estoque_no_pedido: Optional[int]
