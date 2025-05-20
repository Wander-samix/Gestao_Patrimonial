from dataclasses import dataclass
from typing import Optional

@dataclass
class Fornecedor:
    id: Optional[int]
    nome: str
    cnpj: Optional[str]
    endereco: Optional[str]
    telefone: Optional[str]
    email: Optional[str]
    ativo: bool
