from dataclasses import dataclass

@dataclass
class CreateSaidaProdutoPorPedidoDTO:
    produto_id: int
    pedido_id:   int
    quantidade:  int

@dataclass
class SaidaProdutoPorPedidoDTO:
    id:          int
    produto_id:  int
    pedido_id:   int
    quantidade:  int
    data_saida:  str  # ISO datetime
