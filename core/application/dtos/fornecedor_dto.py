# core/application/dtos/fornecedor_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateFornecedorDTO:
    nome: str
    cnpj: Optional[str] = None
    endereco: Optional[str] = ""
    telefone: Optional[str] = None
    email: Optional[str] = None
    ativo: bool = True

@dataclass
class FornecedorDTO:
    id: int
    nome: str
    cnpj: Optional[str]
    endereco: str
    telefone: Optional[str]
    email: Optional[str]
    ativo: bool
