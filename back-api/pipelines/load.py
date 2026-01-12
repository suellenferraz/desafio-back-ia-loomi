from typing import List, Dict, Tuple
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.paint_repository_impl import PaintRepositoryImpl
from app.infrastructure.services.embedding_service import EmbeddingService
from app.application.use_cases.paint_use_cases import create_paint


def load_paints_to_database(paints: List[Dict]) -> Tuple[int, int, List[str], int]:
    db = next(get_db())
    repository = PaintRepositoryImpl(db)
    embedding_service = EmbeddingService()
    
    created_count = 0
    error_count = 0
    errors_list = []
    skipped_count = 0
    
    existing_paints = repository.get_all(skip=0, limit=10000)
    existing_names = {p.name.lower().strip() for p in existing_paints}
    
    seen_in_batch = set()
    unique_paints = []
    for paint_data in paints:
        paint_name_lower = paint_data["name"].lower().strip()
        if paint_name_lower not in seen_in_batch:
            seen_in_batch.add(paint_name_lower)
            unique_paints.append(paint_data)
    
    print(f"   [{len(unique_paints)}] tintas únicas para processar (removidas {len(paints) - len(unique_paints)} duplicatas do batch)")
    
    for paint_data in unique_paints:
        try:
            paint_name_lower = paint_data["name"].lower().strip()
            
            if paint_name_lower in existing_names:
                skipped_count += 1
                continue
            
            paint = create_paint(
                repository=repository,
                name=paint_data["name"],
                color=paint_data["color"],
                surface_type=paint_data["surface_type"],
                environment=paint_data["environment"],
                finish_type=paint_data["finish_type"],
                features=paint_data["features"],
                line=paint_data["line"],
                embedding_service=embedding_service
            )
            
            existing_names.add(paint.name.lower().strip())
            created_count += 1
            
            if created_count % 10 == 0 or created_count == len(unique_paints):
                print(f"   [{created_count}/{len(unique_paints)}] {paint_data['name']} - {paint_data['color']}")
            
        except ValueError as e:
            error_count += 1
            error_msg = f"'{paint_data['name']}': {str(e)}"
            errors_list.append(error_msg)
            
        except Exception as e:
            error_count += 1
            error_msg = f"'{paint_data['name']}': {str(e)}"
            errors_list.append(error_msg)
    
    db.close()
    
    return created_count, error_count, errors_list, skipped_count
