# core/application/dtos/configuracao_estoque_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateConfiguracaoEstoqueDTO:
    area_id: Optional[int]
    estoque_minimo: int

@dataclass
class ConfiguracaoEstoqueDTO:
    id: int
    area_id: Optional[int]
    estoque_minimo: int
