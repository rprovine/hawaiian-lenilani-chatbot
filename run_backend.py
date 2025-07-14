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

# Add api_backend to Python path so imports work correctly
api_backend_dir = os.path.join(project_root, 'api_backend')
sys.path.insert(0, api_backend_dir)

# Print Python path for debugging
print(f"Project root: {project_root}")
print(f"API backend dir: {api_backend_dir}")
print(f"Python path: {sys.path[:3]}")

# Run the server
if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable (Railway provides this)
    port = int(os.environ.get("PORT", 8000))
    
    print("🌺 Starting Hawaiian LeniLani Chatbot API...")
    print(f"🌴 Visit http://localhost:{port} to test the API")
    print(f"📖 API docs available at http://localhost:{port}/docs")
    print("🤙 Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "api_backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )