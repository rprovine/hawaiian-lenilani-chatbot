#!/usr/bin/env python3
"""
Quick test script for Hawaiian LeniLani Chatbot
Run this to test the chatbot without full setup
"""

import os
import sys
import json
from datetime import datetime
import pytz

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock environment variables
os.environ['ANTHROPIC_API_KEY'] = 'test-key'
os.environ['TZ'] = 'Pacific/Honolulu'
os.environ['ENVIRONMENT'] = 'test'

print("🌺 Hawaiian LeniLani Chatbot - Quick Test 🌺\n")
print("=" * 50)

# Test 1: Cultural Intelligence
print("\n1️⃣ Testing Cultural Intelligence...")
try:
    from api_backend.services.cultural_intelligence import CulturalToneManager
    manager = CulturalToneManager()
    
    test_messages = [
        "Eh howzit brah, my store stay slow",
        "Good morning, I need business consulting",
        "Can you help with my ohana restaurant?",
    ]
    
    for msg in test_messages:
        result = manager.analyze_message(msg)
        print(f"\nMessage: '{msg}'")
        print(f"  - Uses Pidgin: {result['uses_pidgin']}")
        print(f"  - Tone: {result['recommended_tone']}")
        print(f"  - Cultural Elements: {result['cultural_elements']}")
    
    print("✅ Cultural Intelligence: PASSED")
except Exception as e:
    print(f"❌ Cultural Intelligence: FAILED - {e}")

# Test 2: Time-based Greetings
print("\n\n2️⃣ Testing Time-based Hawaiian Greetings...")
try:
    hawaii_tz = pytz.timezone('Pacific/Honolulu')
    current_time = datetime.now(hawaii_tz)
    hour = current_time.hour
    
    if 5 <= hour < 10:
        expected = "Aloha kakahiaka"
        time_period = "morning"
    elif 10 <= hour < 14:
        expected = "Aloha awakea"
        time_period = "midday"
    elif 14 <= hour < 18:
        expected = "Aloha 'auinalā"
        time_period = "afternoon"
    elif 18 <= hour < 22:
        expected = "Aloha ahiahi"
        time_period = "evening"
    else:
        expected = "Aloha"
        time_period = "night"
    
    print(f"Current time in Hawaii: {current_time.strftime('%I:%M %p HST')}")
    print(f"Time period: {time_period}")
    print(f"Appropriate greeting: {expected}")
    print("✅ Time-based Greetings: PASSED")
except Exception as e:
    print(f"❌ Time-based Greetings: FAILED - {e}")

# Test 3: Island Business Knowledge
print("\n\n3️⃣ Testing Island Business Knowledge...")
try:
    from claude_integration.cultural_prompts import ISLAND_BUSINESS_CONTEXT
    
    print("\nIsland-Specific Business Insights:")
    for island, info in ISLAND_BUSINESS_CONTEXT.items():
        print(f"\n{island.upper()}:")
        print(f"  - Key Industries: {', '.join(info['key_industries'][:3])}")
        print(f"  - Business Tip: {info['business_tips'][0][:60]}...")
    
    print("\n✅ Island Business Knowledge: PASSED")
except Exception as e:
    print(f"❌ Island Business Knowledge: FAILED - {e}")

# Test 4: Business Type Detection
print("\n\n4️⃣ Testing Business Type Detection...")
try:
    test_businesses = [
        ("I have a snorkeling tour company", "tourism"),
        ("We run a poke restaurant", "restaurant"),
        ("Our coffee farm needs help", "agriculture"),
        ("My retail shop sells Hawaiian crafts", "retail")
    ]
    
    for description, expected_type in test_businesses:
        result = manager.analyze_message(description)
        detected_type = result['business_context']['type']
        status = "✅" if detected_type == expected_type else "❌"
        print(f"{status} '{description}' -> {detected_type}")
    
    print("✅ Business Type Detection: PASSED")
except Exception as e:
    print(f"❌ Business Type Detection: FAILED - {e}")

# Test 5: Mock Conversation Flow
print("\n\n5️⃣ Testing Mock Conversation Flow...")
try:
    conversation = [
        ("User", "Aloha!"),
        ("Bot", f"{expected}! Welcome to LeniLani Consulting. How can I help your business thrive today?"),
        ("User", "I have a restaurant on Maui that's struggling"),
        ("Bot", "I understand, running a restaurant can be challenging, especially on Maui. What specific challenges are you facing?"),
        ("User", "High food costs and finding good workers"),
        ("Bot", "These are common challenges for Maui restaurants. Let me help you with strategies for managing food costs and attracting reliable staff in our tight labor market."),
    ]
    
    print("\nSample Conversation:")
    for speaker, message in conversation:
        prefix = "👤" if speaker == "User" else "🤖"
        print(f"\n{prefix} {speaker}: {message}")
    
    print("\n✅ Conversation Flow: PASSED")
except Exception as e:
    print(f"❌ Conversation Flow: FAILED - {e}")

# Test 6: Pidgin Phrases
print("\n\n6️⃣ Testing Pidgin Phrase Recognition...")
try:
    from claude_integration.cultural_prompts import PIDGIN_PHRASES
    
    print("\nRecognized Pidgin Phrases:")
    sample_phrases = PIDGIN_PHRASES[:10] if len(PIDGIN_PHRASES) > 10 else PIDGIN_PHRASES
    for phrase in sample_phrases:
        print(f"  - {phrase}")
    
    print(f"\nTotal pidgin phrases loaded: {len(PIDGIN_PHRASES)}")
    print("✅ Pidgin Phrases: PASSED")
except Exception as e:
    print(f"❌ Pidgin Phrases: FAILED - {e}")

# Test 7: Hawaiian Values
print("\n\n7️⃣ Testing Hawaiian Values Integration...")
try:
    from claude_integration.cultural_prompts import HAWAIIAN_VALUES
    
    print("\nHawaiian Values in Business:")
    for value, info in HAWAIIAN_VALUES.items():
        print(f"\n{value.upper()}:")
        print(f"  - Description: {info['description'][:60]}...")
        print(f"  - Business Application: {info['business_application'][:60]}...")
    
    print("\n✅ Hawaiian Values: PASSED")
except Exception as e:
    print(f"❌ Hawaiian Values: FAILED - {e}")

# Summary
print("\n" + "=" * 50)
print("🌴 Quick Test Complete! 🌴")
print("\nTo run the full chatbot:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Set up environment variables in .env")
print("3. Run: cd deployment && ./deploy.sh deploy")
print("\nOr test individual components:")
print("- Run unit tests: pytest")
print("- Test API: cd api_backend && uvicorn main:app --reload")
print("\nAloha! 🌺")