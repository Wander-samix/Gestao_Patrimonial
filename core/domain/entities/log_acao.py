from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class LogAcao:
    id: Optional[int]
    usuario_id: Optional[int]
    acao: str
    detalhes: Optional[str]
    data_hora: datetime
    ip: Optional[str]
