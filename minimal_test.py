#!/usr/bin/env python3
"""
Minimal test script for Hawaiian LeniLani Chatbot
Tests basic functionality without full dependencies
"""

import os
import sys
from datetime import datetime
import pytz

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🌺 Hawaiian LeniLani Chatbot - Minimal Test 🌺\n")
print("=" * 50)

# Test 1: Basic imports
print("\n1️⃣ Testing Basic Imports...")
try:
    import anthropic
    print("✅ Anthropic SDK imported successfully")
except ImportError as e:
    print(f"❌ Anthropic import failed: {e}")

try:
    import fastapi
    print("✅ FastAPI imported successfully")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")

try:
    import uvicorn
    print("✅ Uvicorn imported successfully")
except ImportError as e:
    print(f"❌ Uvicorn import failed: {e}")

# Test 2: Time-based Greetings
print("\n\n2️⃣ Testing Time-based Hawaiian Greetings...")
try:
    hawaii_tz = pytz.timezone('Pacific/Honolulu')
    current_time = datetime.now(hawaii_tz)
    hour = current_time.hour
    
    if 5 <= hour < 10:
        greeting = "Aloha kakahiaka"
        time_period = "morning"
    elif 10 <= hour < 14:
        greeting = "Aloha awakea"
        time_period = "midday"
    elif 14 <= hour < 18:
        greeting = "Aloha 'auinalā"
        time_period = "afternoon"
    elif 18 <= hour < 22:
        greeting = "Aloha ahiahi"
        time_period = "evening"
    else:
        greeting = "Aloha"
        time_period = "night"
    
    print(f"Current time in Hawaii: {current_time.strftime('%I:%M %p HST')}")
    print(f"Time period: {time_period}")
    print(f"Appropriate greeting: {greeting}")
    print("✅ Time-based Greetings: PASSED")
except Exception as e:
    print(f"❌ Time-based Greetings: FAILED - {e}")

# Test 3: Check for API Backend
print("\n\n3️⃣ Checking API Backend Structure...")
try:
    import api_backend
    print("✅ API Backend package found")
    
    # Check for main.py
    if os.path.exists("api_backend/main.py"):
        print("✅ API Backend main.py exists")
    else:
        print("❌ API Backend main.py not found")
        
except ImportError:
    print("❌ API Backend package not found")

# Test 4: Check for Frontend
print("\n\n4️⃣ Checking Frontend Structure...")
if os.path.exists("frontend/package.json"):
    print("✅ Frontend package.json exists")
    if os.path.exists("frontend/node_modules"):
        print("✅ Frontend dependencies installed")
    else:
        print("⚠️  Frontend dependencies not installed (run: cd frontend && npm install)")
else:
    print("❌ Frontend package.json not found")

# Test 5: Environment Configuration
print("\n\n5️⃣ Checking Environment Configuration...")
if os.path.exists(".env"):
    print("✅ .env file exists")
    
    # Check for critical environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('ANTHROPIC_API_KEY', '')
    if api_key and api_key != 'your_anthropic_api_key_here':
        print("✅ ANTHROPIC_API_KEY is configured")
    else:
        print("⚠️  ANTHROPIC_API_KEY needs to be set in .env file")
else:
    print("❌ .env file not found")

# Summary
print("\n" + "=" * 50)
print("🌴 Minimal Test Complete! 🌴")
print("\nNext steps:")
print("1. Add your Anthropic API key to the .env file")
print("2. Install Python 3.9 or 3.10 for full Rasa support")
print("3. Set up PostgreSQL and Redis databases")
print("4. Run the API backend: source venv/bin/activate && cd api_backend && uvicorn main:app --reload")
print("5. Run the frontend: cd frontend && npm start")
print("\nAloha! 🌺")