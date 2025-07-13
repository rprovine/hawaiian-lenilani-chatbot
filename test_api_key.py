#!/usr/bin/env python3
"""
Simple test to verify the API key is working
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test if the API key is set
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key or api_key == "your_anthropic_api_key_here":
    print("❌ API key not set properly")
    exit(1)

print("✅ API key is configured")

# Test a simple API call
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=api_key)
    
    # Make a simple test call
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=50,
        messages=[{"role": "user", "content": "Say hello from Hawaii"}]
    )
    
    print("✅ API connection working")
    print(f"Response: {response.content[0].text}")
    
except Exception as e:
    print(f"❌ API connection failed: {e}")
    exit(1)

print("\n🌺 All tests passed! The chatbot should work now.")
