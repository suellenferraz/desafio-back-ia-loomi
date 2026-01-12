from fastapi import APIRouter
from app.presentation.api.schemas.product_schema import ProductResponseSchema
from app.application.use_cases.product_use_cases import get_product_example

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/{product_id}", response_model=ProductResponseSchema)
def get_product(product_id: int):
    """Rota de exemplo - busca um produto"""
    product = get_product_example(product_id)
    return ProductResponseSchema.model_validate(product)

