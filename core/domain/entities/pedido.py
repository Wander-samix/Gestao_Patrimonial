from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Pedido:
    id: Optional[int]
    codigo: str
    usuario_id: int
    data_solicitacao: datetime
    status: str
    aprovado_por_id: Optional[int]
    data_separacao: Optional[datetime]
    data_retirada: Optional[datetime]
    retirado_por: Optional[str]
    observacao: Optional[str]
    data_necessaria: Optional[date]
    data_aprovacao: Optional[datetime]
