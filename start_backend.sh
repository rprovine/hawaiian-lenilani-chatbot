#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
cd api_backend
python -m uvicorn main:app --reload --port 8000