import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()
