from typing import List, Dict


def transform_paints_data(raw_data: Dict) -> List[Dict]:
    products = raw_data["products"]
    colors = raw_data["colors"]
    
    transformed_paints = []
    
    for product in products:
        if product["line"] == "Premium":
            product_colors = colors
        else:
            product_colors = colors[:8]
        
        for color in product_colors:
            if product.get("variant"):
                full_name = f"{product['base_name']} {product['variant']}"
            else:
                full_name = product["base_name"]
            
            if color["name"] != "Branco Neve":
                paint_name = f"{full_name} {color['name']}"
            else:
                paint_name = full_name
            
            transformed_paint = {
                "name": paint_name,
                "color": color["name"],
                "surface_type": product["surface_type"],
                "environment": product["environment"],
                "finish_type": product["finish_type"],
                "features": product["features"].copy(),
                "line": product["line"]
            }
            
            transformed_paints.append(transformed_paint)
    
    return transformed_paints


def validate_paint_data(paint: Dict) -> bool:
    required_fields = ["name", "color", "surface_type", "environment", "finish_type", "features", "line"]
    
    for field in required_fields:
        if field not in paint:
            return False
    
    if paint["environment"] not in ["interno", "externo"]:
        return False
    
    if not isinstance(paint["features"], list):
        return False
    
    return True
