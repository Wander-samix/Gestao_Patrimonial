from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CreateUsuarioDTO:
    username: str
    password: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    matricula: Optional[str] = None
    papel: Optional[str] = None
    ativo: Optional[bool] = True
    areas_ids: Optional[List[int]] = None
    groups_ids: Optional[List[int]] = None
    user_permissions_ids: Optional[List[int]] = None

@dataclass
class UsuarioDTO:
    id: int
    username: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    matricula: Optional[str]
    papel: str
    ativo: bool
    areas_ids: List[int]
    groups_ids: List[int]
    user_permissions_ids: List[int]
