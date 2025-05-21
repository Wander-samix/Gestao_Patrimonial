# core/application/dtos/cliente_dto.py
from dataclasses import dataclass

@dataclass
class CreateClienteDTO:
    matricula: str
    nome_completo: str
    email: str
    telefone: str
    curso: str

@dataclass
class ClienteDTO:
    id: int
    matricula: str
    nome_completo: str
    email: str
    telefone: str
    curso: str
