from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CreateLogAcaoDTO:
    usuario_id: Optional[int] = None
    acao: str = ""
    detalhes: str = ""
    data_hora: Optional[datetime] = None
    ip: Optional[str] = None

@dataclass
class LogAcaoDTO:
    id: int
    usuario_id: Optional[int]
    acao: str
    detalhes: str
    data_hora: Optional[datetime]
    ip: Optional[str]
