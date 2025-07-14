#!/usr/bin/env python3
"""Run the backend API server"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Don't change directory, run from project root
# Add api_backend to Python path
api_backend_dir = os.path.join(project_root, 'api_backend')
sys.path.insert(0, api_backend_dir)

# Run the server
if __name__ == "__main__":
    import uvicorn
    print("🌺 Starting Hawaiian LeniLani Chatbot API...")
    print("🌴 Visit http://localhost:8000 to test the API")
    print("📖 API docs available at http://localhost:8000/docs")
    print("🤙 Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "api_backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )