#!/usr/bin/env python3
"""Test Claude integration directly"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from claude_integration.hawaiian_claude_client import HawaiianClaudeClient

def test_claude():
    """Test basic Claude functionality"""
    try:
        print("🌺 Testing Hawaiian Claude Client...")
        
        # Initialize client
        client = HawaiianClaudeClient()
        print("✅ Client initialized successfully")
        
        # Test greeting generation
        greeting = client.generate_cultural_greeting("Test User")
        print(f"✅ Greeting generated: {greeting}")
        
        # Test basic response
        response = client.generate_response(
            user_message="Aloha! Tell me about your services for Hawaiian businesses.",
            conversation_history=[],
            business_context={},
            cultural_mode="authentic"
        )
        print(f"✅ Response generated: {response['response'][:200]}...")
        
        # Test business inquiry
        business_response = client.handle_business_inquiry(
            business_type="restaurant",
            island="Maui",
            challenges=["tourist vs local balance", "inventory management"],
            conversation_history=[]
        )
        print(f"✅ Business inquiry handled: {business_response['response'][:200]}...")
        
        print("\n🎉 All tests passed! Claude integration is working properly.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_claude()