#!/bin/bash

echo "🌺 Starting Hawaiian LeniLani Backend"
echo "===================================="

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Navigate to project root
cd "$(dirname "$0")"

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Navigate to api_backend directory
cd api_backend

# Set Python path to include api_backend directory
export PYTHONPATH="$PWD:$PYTHONPATH"

# Load environment variables
echo "🔐 Loading environment variables..."
set -a
source ../.env
set +a

# Start the backend
echo "🚀 Starting backend on port 8000..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload