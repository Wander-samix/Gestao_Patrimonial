from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class CreatePedidoDTO:
    codigo: str
    usuario_id: int
    data_necessaria: Optional[date] = None
    observacao: Optional[str] = None

@dataclass
class PedidoDTO:
    id: int
    codigo: str
    usuario_id: int
    data_solicitacao: date
    status: str
    data_necessaria: Optional[date]
    observacao: Optional[str]
