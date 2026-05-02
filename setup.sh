#!/bin/bash

echo "============================================"
echo "  Food Delivery Pipeline - Setup"
echo "============================================"
echo ""

if [ ! -d ".venv" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv .venv
else
    echo "[1/3] Virtual environment exists ✅"
fi

echo "[2/3] Activating and installing dependencies..."
source .venv/bin/activate
pip install -q pandas matplotlib

echo "[3/3] Verifying installation..."
python3 -c "import pandas; import matplotlib; print('  pandas', pandas.__version__); print('  matplotlib', matplotlib.__version__)"

echo ""
echo "============================================"
echo "  Setup complete! Run the pipeline with:"
echo "  source .venv/bin/activate && python3 run.py"
echo "============================================"
