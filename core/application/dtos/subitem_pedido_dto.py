from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateSubitemPedidoDTO:
    pedido_id: int
    produto_id: int
    quantidade: int
    estoque_no_pedido: Optional[int] = None

@dataclass
class SubitemPedidoDTO:
    id: int
    pedido_id: int
    produto_id: int
    quantidade: int
    estoque_no_pedido: Optional[int]
