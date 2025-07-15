#!/usr/bin/env python3
"""Test that lead capture creates only one lead per session"""
import asyncio
import logging
from api_backend.services.hawaiian_conversation_router import HawaiianConversationRouter

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_single_lead_capture():
    """Test that multiple contact info pieces result in one lead"""
    
    # Create router
    router = HawaiianConversationRouter()
    
    # Create a session
    session_id = "test_session_123"
    
    print("=== Testing Single Lead Capture ===\n")
    
    # Message 1: Introduction with name
    print("1. Sending message with name...")
    response = await router.route_message(
        "Hi, my name is John Smith",
        session_id=session_id
    )
    print(f"Response: {response['response'][:100]}...")
    
    # Check session state
    session = router.sessions[session_id]
    print(f"Lead data after name: {session.get('lead_data', {})}")
    print(f"Lead captured: {session.get('lead_captured', False)}\n")
    
    # Message 2: Add email
    print("2. Sending message with email...")
    response = await router.route_message(
        "My email is john@smithconstruction.com",
        session_id=session_id
    )
    print(f"Response: {response['response'][:100]}...")
    
    # Check session state
    print(f"Lead data after email: {session.get('lead_data', {})}")
    print(f"Lead captured: {session.get('lead_captured', False)}\n")
    
    # Message 3: Add company name
    print("3. Sending message with company...")
    response = await router.route_message(
        "I own Smith Construction Company on Oahu",
        session_id=session_id
    )
    print(f"Response: {response['response'][:100]}...")
    
    # Check session state
    print(f"Lead data after company: {session.get('lead_data', {})}")
    print(f"Lead captured: {session.get('lead_captured', False)}\n")
    
    # Message 4: Add phone number (this should trigger capture)
    print("4. Sending message with phone...")
    response = await router.route_message(
        "You can reach me at 808-555-1234",
        session_id=session_id
    )
    print(f"Response: {response['response'][:100]}...")
    
    # Check final session state
    print(f"Lead data after phone: {session.get('lead_data', {})}")
    print(f"Lead captured: {session.get('lead_captured', False)}")
    print(f"Lead ID: {session.get('lead_id', 'Not set')}\n")
    
    # Wait a bit for async lead capture to complete
    await asyncio.sleep(2)
    
    # Check final state
    print("=== Final Results ===")
    print(f"Lead captured: {session.get('lead_captured', False)}")
    print(f"Lead ID: {session.get('lead_id', 'Not captured')}")
    print(f"Final lead data: {session.get('lead_data', {})}")
    
    # Check lead files
    import os
    import glob
    lead_files = glob.glob("logs/leads/*.json")
    print(f"\nLead files created: {len(lead_files)}")
    if lead_files:
        print("Lead files:")
        for f in sorted(lead_files)[-5:]:  # Show last 5
            print(f"  - {os.path.basename(f)}")

if __name__ == "__main__":
    asyncio.run(test_single_lead_capture())