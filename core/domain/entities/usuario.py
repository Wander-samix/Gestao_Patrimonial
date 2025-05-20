from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Usuario:
    id: Optional[int]
    username: str
    first_name: str
    last_name: str
    email: str
    matricula: Optional[str]
    papel: str
    ativo: bool
    areas: List[int]  # IDs de Area

    def todas_areas(self, todas_areas_ids: List[int]) -> List[int]:
        """
        Se for admin ou técnico, retorna todas as áreas (IDs),
        caso contrário, apenas as áreas associadas.
        """
        if self.papel in ('admin', 'tecnico'):
            return todas_areas_ids
        return self.areas
