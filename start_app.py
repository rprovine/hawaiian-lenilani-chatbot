#!/usr/bin/env python3
"""Start the Hawaiian LeniLani Chatbot Backend"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Now we can import and run the app
if __name__ == "__main__":
    import uvicorn
    
    print("🌺 Starting Hawaiian LeniLani Chatbot API...")
    print("🌴 API will be available at: http://localhost:8000")
    print("📖 API docs available at: http://localhost:8000/docs")
    print("🤙 Press Ctrl+C to stop the server\n")
    
    # Try different port if 8000 is in use
    port = 8000
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    
    if result == 0:
        port = 8001
        print(f"⚠️  Port 8000 is in use, using port {port} instead")
    
    uvicorn.run(
        "api_backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )