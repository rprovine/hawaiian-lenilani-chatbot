#!/usr/bin/env python3
"""Test the full application stack"""
import os
import sys
import time
import requests
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Backend health check passed")
            print(f"   Response: {response.json()}")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running")
    return False

def test_chat_endpoint():
    """Test chat endpoint"""
    try:
        payload = {
            "message": "Aloha! Tell me about your services.",
            "session_id": "test-session-123"
        }
        response = requests.post("http://localhost:8000/chat", json=payload)
        if response.status_code == 200:
            print("✅ Chat endpoint working")
            data = response.json()
            print(f"   Response preview: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat endpoint error: {str(e)}")
    return False

def test_services_endpoint():
    """Test services endpoint"""
    try:
        response = requests.get("http://localhost:8000/services")
        if response.status_code == 200:
            print("✅ Services endpoint working")
            data = response.json()
            print(f"   Found {len(data.get('services', {}))} services")
            return True
    except Exception as e:
        print(f"❌ Services endpoint error: {str(e)}")
    return False

def main():
    print("🌺 Hawaiian LeniLani Chatbot - Full Application Test")
    print("=" * 50)
    
    # Check if backend is running
    print("\n📡 Testing Backend API...")
    backend_running = test_backend_health()
    
    if not backend_running:
        print("\n🚀 Starting backend server...")
        # Start backend in background
        backend_process = subprocess.Popen(
            [sys.executable, "run_backend.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("   Waiting for backend to start...")
        time.sleep(5)  # Give it time to start
        
        # Retry health check
        backend_running = test_backend_health()
    
    if backend_running:
        print("\n🧪 Running API tests...")
        chat_test = test_chat_endpoint()
        services_test = test_services_endpoint()
        
        print("\n📊 Test Summary:")
        print(f"   - Backend Health: {'✅' if backend_running else '❌'}")
        print(f"   - Chat Endpoint: {'✅' if chat_test else '❌'}")
        print(f"   - Services Endpoint: {'✅' if services_test else '❌'}")
        
        if all([backend_running, chat_test, services_test]):
            print("\n🎉 All backend tests passed!")
            print("\n📱 Frontend Information:")
            print("   - To start frontend: cd frontend && npm start")
            print("   - Frontend will be available at: http://localhost:3000")
            print("   - Chat widget will automatically connect to backend")
            print("\n🌴 Your Hawaiian LeniLani Chatbot is ready to use!")
        else:
            print("\n⚠️  Some tests failed. Please check the errors above.")
    else:
        print("\n❌ Could not start backend. Please check:")
        print("   1. Python dependencies are installed (pip install -r requirements-minimal.txt)")
        print("   2. .env file exists with ANTHROPIC_API_KEY")
        print("   3. No other process is using port 8000")

if __name__ == "__main__":
    main()