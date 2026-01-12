from typing import List, Dict


def extract_suvinil_paints() -> Dict:
    products = [
        {
            "product_line": "Toque",
            "variant": "Brilho",
            "base_name": "Suvinil Toque",
            "environment": "interno",
            "surface_type": "parede, concreto, gesso",
            "finish_type": "semibrilho",
            "features": ["lavável", "resistente à limpeza", "intensifica cores"],
            "line": "Premium"
        },
        {
            "product_line": "Toque",
            "variant": "Seda",
            "base_name": "Suvinil Toque",
            "environment": "interno",
            "surface_type": "parede, concreto, gesso",
            "finish_type": "acetinado",
            "features": ["lavável", "resistente à limpeza", "disfarce de imperfeições"],
            "line": "Premium"
        },
        {
            "product_line": "Toque",
            "variant": "Fosco",
            "base_name": "Suvinil Toque",
            "environment": "interno",
            "surface_type": "parede, concreto, gesso",
            "finish_type": "fosco",
            "features": ["lavável", "fácil retoque"],
            "line": "Premium"
        },
        {
            "product_line": "Toque",
            "variant": "Fosco Completo",
            "base_name": "Suvinil Toque",
            "environment": "interno",
            "surface_type": "parede, concreto, gesso",
            "finish_type": "fosco",
            "features": ["lavável", "disfarce de imperfeições", "superliso"],
            "line": "Premium"
        },
        {
            "product_line": "Inova",
            "variant": "Fosco Sempre Limpo",
            "base_name": "Suvinil Inova",
            "environment": "interno",
            "surface_type": "parede, concreto, gesso",
            "finish_type": "fosco",
            "features": ["lavável", "alta resistência à limpeza", "disfarce de imperfeições"],
            "line": "Premium"
        },
        {
            "product_line": "Fachada Protegida",
            "variant": "Standard",
            "base_name": "Suvinil Fachada Protegida",
            "environment": "externo",
            "surface_type": "concreto, alvenaria",
            "finish_type": "fosco",
            "features": ["resistente à chuva", "proteção UV", "antimofo", "antipoluição"],
            "line": "Standard"
        },
        {
            "product_line": "Acrílica",
            "variant": "Standard",
            "base_name": "Suvinil Acrílica",
            "environment": "interno",
            "surface_type": "concreto, gesso, madeira",
            "finish_type": "fosco",
            "features": ["antimofo", "proteção alta para mofo", "baixo odor"],
            "line": "Standard"
        },
        {
            "product_line": "Esmalte",
            "variant": "Multissuperfícies",
            "base_name": "Esmalte Suvinil",
            "environment": "interno",
            "surface_type": "madeira, metal, azulejo, pastilha, vidro, alvenaria",
            "finish_type": "acetinado",
            "features": ["antimofo", "secagem rápida", "fácil aplicação", "à base de água"],
            "line": "Premium"
        },
    ]
    
    colors = [
        {"name": "Branco Neve", "category": "neutro"},
        {"name": "Azul Sereno", "category": "suave"},
        {"name": "Verde Garrafa", "category": "vibrante"},
        {"name": "Cerrado", "category": "bege"},
        {"name": "Estátua de Bronze", "category": "bege"},
        {"name": "Lenço de Bolso", "category": "suave"},
        {"name": "Flan de Baunilha", "category": "bege"},
        {"name": "Cinza Pérola", "category": "neutro"},
        {"name": "Branco Gelo", "category": "neutro"},
        {"name": "Azul Celeste", "category": "suave"},
        {"name": "Verde Limão", "category": "vibrante"},
        {"name": "Rosa Pêssego", "category": "suave"},
        {"name": "Amarelo Sol", "category": "vibrante"},
        {"name": "Laranja Tangerina", "category": "vibrante"},
        {"name": "Vermelho Carmim", "category": "vibrante"},
    ]
    
    return {"products": products, "colors": colors}
