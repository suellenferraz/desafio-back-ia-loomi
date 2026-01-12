from dataclasses import dataclass

@dataclass
class Product:
    """Entidade de domínio Product"""
    id: int
    name: str
    price: float

