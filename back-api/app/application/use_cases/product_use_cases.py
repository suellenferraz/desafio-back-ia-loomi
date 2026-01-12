from app.domain.entities.product import Product

def get_product_example(product_id: int) -> Product:
    """Exemplo simples de serviço da camada application"""
    return Product(id=product_id, name="Produto Exemplo", price=99.99)

