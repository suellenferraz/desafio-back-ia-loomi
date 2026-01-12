import sys
import os

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pipelines.pipeline import run_etl_pipeline

if __name__ == "__main__":
    try:
        results = run_etl_pipeline()
        
        if results["errors"] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
