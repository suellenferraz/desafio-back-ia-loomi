from typing import Dict
from .extract import extract_suvinil_paints
from .transform import transform_paints_data, validate_paint_data
from .enrich import enrich_paints_with_ai
from .load import load_paints_to_database


def run_etl_pipeline() -> Dict:
    print("=" * 60)
    print("ETL PIPELINE - TINTAS SUVINIL")
    print("=" * 60)
    
    print("\n[EXTRACT] Extraindo dados...")
    raw_data = extract_suvinil_paints()
    print(f"   [{len(raw_data['products'])}] produtos base")
    print(f"   [{len(raw_data['colors'])}] cores disponíveis")
    
    print("\n[TRANSFORM] Criando variações...")
    transformed_paints = transform_paints_data(raw_data)
    print(f"   [{len(transformed_paints)}] variações criadas")
    
    print("\n[ENRICH] Enriquecendo com IA...")
    enriched_paints = enrich_paints_with_ai(transformed_paints)
    print(f"   [{len(enriched_paints)}] variações após enriquecimento")
    
    valid_paints = [p for p in enriched_paints if validate_paint_data(p)]
    print(f"   [{len(valid_paints)}] tintas válidas")
    
    print("\n[LOAD] Carregando no banco...")
    created, errors, error_list, skipped = load_paints_to_database(valid_paints)
    
    print("\n" + "=" * 60)
    print("ETL CONCLUÍDO")
    print("=" * 60)
    print("Estatísticas:")
    print(f"  - Extraídos: {len(raw_data['products'])} produtos base")
    print(f"  - Transformados: {len(transformed_paints)} variações")
    print(f"  - Criadas: {created}")
    print(f"  - Já existentes: {skipped}")
    print(f"  - Erros: {errors}")
    
    if errors > 0 and error_list:
        print("\n[AVISO] Primeiros erros:")
        for error in error_list[:3]:
            print(f"  - {error}")
    
    return {
        "extracted": len(raw_data['products']),
        "transformed": len(transformed_paints),
        "created": created,
        "skipped": skipped,
        "errors": errors
    }
