#!/usr/bin/env python3
"""Test lead extraction directly"""
import re
from api_backend.services.hawaiian_conversation_router import HawaiianConversationRouter

def test_lead_extraction():
    router = HawaiianConversationRouter()
    
    # Test message with email
    test_message = "Hello I need help with inventory management. My email is sarah@kahikomarket.com"
    
    # Create a test session
    test_session = {
        "conversation_history": [],
        "business_context": {}
    }
    
    # Test extraction
    lead_info = router._extract_lead_info(test_message, [], test_session)
    
    print(f"Message: {test_message}")
    print(f"Extracted lead info: {lead_info}")
    
    # Test email pattern directly
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, test_message)
    print(f"Direct email match: {email_match.group() if email_match else None}")

if __name__ == "__main__":
    test_lead_extraction()