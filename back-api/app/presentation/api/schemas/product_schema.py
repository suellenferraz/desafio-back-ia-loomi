from pydantic import BaseModel

class ProductResponseSchema(BaseModel):
    """Schema de resposta do produto"""
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

