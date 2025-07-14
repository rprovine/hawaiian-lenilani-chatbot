#!/usr/bin/env python3
import os
import sys
import subprocess

# Change to project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Kill any existing process on port 8000
subprocess.run("lsof -ti:8000 | xargs kill -9 2>/dev/null || true", shell=True)

print("🌺 Starting Hawaiian LeniLani Chatbot...")
print("=" * 50)

# Start backend
print("🚀 Starting backend server...")
backend_cmd = [
    sys.executable, "-m", "uvicorn", 
    "api_backend.main:app", 
    "--host", "0.0.0.0", 
    "--port", "8000"
]

try:
    subprocess.run(backend_cmd)
except KeyboardInterrupt:
    print("\n🌙 Shutting down... A hui hou!")