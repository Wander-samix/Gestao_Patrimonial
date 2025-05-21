from dataclasses import dataclass

@dataclass
class CreateAreaDTO:
    nome: str

@dataclass
class AreaDTO:
    id: int
    nome: str
