from dataclasses import dataclass
from typing import Optional

@dataclass
class ConfiguracaoEstoque:
    id: Optional[int]
    area_id: Optional[int]
    estoque_minimo: int
