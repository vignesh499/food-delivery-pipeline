import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingest import ingest_all
from transform import transform_all
from load import load_all
from analytics import run_analytics

try:
    from visualize import generate_all_visualizations
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def run_pipeline():
    print("=" * 60)
    print("  FOOD DELIVERY DATA PIPELINE")
    print("=" * 60)

    start_time = time.time()

    print("\n--- STAGE 1: INGESTION ---")
    stage_start = time.time()
    orders, customers, restaurants = ingest_all()
    print(f"⏱  Ingestion completed in {time.time() - stage_start:.2f}s\n")

    print("--- STAGE 2: TRANSFORMATION ---")
    stage_start = time.time()
    orders, customers, restaurants = transform_all(orders, customers, restaurants)
    print(f"⏱  Transformation completed in {time.time() - stage_start:.2f}s\n")

    print("--- STAGE 3: LOADING ---")
    stage_start = time.time()
    db_path = load_all(orders, customers, restaurants)
    print(f"⏱  Loading completed in {time.time() - stage_start:.2f}s\n")

    print("--- STAGE 4: ANALYTICS ---")
    stage_start = time.time()
    run_analytics(db_path)
    print(f"⏱  Analytics completed in {time.time() - stage_start:.2f}s\n")

    if HAS_MATPLOTLIB:
        print("--- STAGE 5: VISUALIZATION ---")
        stage_start = time.time()
        generate_all_visualizations(db_path)
        print(f"⏱  Visualization completed in {time.time() - stage_start:.2f}s\n")
    else:
        print("--- STAGE 5: VISUALIZATION (SKIPPED) ---")
        print("  matplotlib not installed. Run: pip install matplotlib\n")

    total_time = time.time() - start_time
    print("=" * 60)
    print(f"  PIPELINE COMPLETE — Total time: {total_time:.2f}s")
    print(f"  Database: {db_path}")
    if HAS_MATPLOTLIB:
        print(f"  Charts:   data/visualizations/")
    print("=" * 60)


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    run_pipeline()
