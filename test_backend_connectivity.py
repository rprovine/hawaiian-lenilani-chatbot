#!/usr/bin/env python3
"""
Test script to check backend connectivity
"""
import requests
import json
import sys

def test_backend(url):
    """Test backend endpoints"""
    print(f"Testing backend at: {url}")
    print("=" * 50)
    
    # Remove trailing slash
    url = url.rstrip('/')
    
    # Test 1: Health endpoint
    print("1. Testing /health endpoint...")
    try:
        response = requests.get(f"{url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
            print("   ✅ Health check PASSED")
        else:
            print(f"   ❌ Health check FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Health check ERROR: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2. Testing / (root) endpoint...")
    try:
        response = requests.get(f"{url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
            print("   ✅ Root endpoint PASSED")
        else:
            print(f"   ❌ Root endpoint FAILED: {response.text}")
    except Exception as e:
        print(f"   ❌ Root endpoint ERROR: {e}")
    
    # Test 3: Logo endpoint
    print("\n3. Testing /logo endpoint...")
    try:
        response = requests.get(f"{url}/logo", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
            print("   ✅ Logo endpoint PASSED")
        else:
            print(f"   ❌ Logo endpoint FAILED: {response.text}")
    except Exception as e:
        print(f"   ❌ Logo endpoint ERROR: {e}")
    
    # Test 4: Chat endpoint
    print("\n4. Testing /chat endpoint...")
    try:
        chat_data = {
            "message": "Aloha",
            "session_id": "test-session"
        }
        response = requests.post(
            f"{url}/chat", 
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
            print("   ✅ Chat endpoint PASSED")
        else:
            print(f"   ❌ Chat endpoint FAILED: {response.text}")
    except Exception as e:
        print(f"   ❌ Chat endpoint ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("Backend test completed!")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_backend_connectivity.py <backend_url>")
        print("Example: python test_backend_connectivity.py https://your-app.onrender.com")
        sys.exit(1)
    
    backend_url = sys.argv[1]
    test_backend(backend_url)