#!/usr/bin/env python3
"""Test backend API directly"""
import os
import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import FastAPI app
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api_backend'))
sys.path.insert(0, os.getcwd())

import uvicorn
from main import app

if __name__ == "__main__":
    print("🌺 Starting Hawaiian LeniLani Chatbot API...")
    print("🌴 Visit http://localhost:8000 to test the API")
    print("📖 API docs available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)