from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    id: Optional[int]
    matricula: str
    nome_completo: str
    email: str
    telefone: str
    curso: str
