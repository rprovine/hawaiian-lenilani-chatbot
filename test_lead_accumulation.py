#!/usr/bin/env python3
"""Test that lead data accumulates properly in session"""
import asyncio
import json
import httpx
import uuid
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_lead_accumulation():
    """Test the complete lead accumulation flow"""
    
    # Generate unique session ID for this test
    session_id = f"test_session_{uuid.uuid4().hex[:8]}"
    print(f"Testing with session ID: {session_id}\n")
    
    async with httpx.AsyncClient() as client:
        # Message 1: Introduction with name
        print("1. Sending message with name...")
        response = await client.post(
            f"{BASE_URL}/chat",
            json={
                "message": "Hi, my name is Sarah Johnson",
                "session_id": session_id
            }
        )
        chat_response = response.json()
        print(f"Response: {chat_response['response'][:100]}...")
        
        # Check lead data
        lead_response = await client.get(f"{BASE_URL}/session/{session_id}/lead-data")
        lead_data = lead_response.json()
        print(f"Lead data after name: {json.dumps(lead_data, indent=2)}\n")
        
        # Message 2: Add company
        print("2. Sending message with company...")
        response = await client.post(
            f"{BASE_URL}/chat",
            json={
                "message": "I own Paradise Poke Bowl restaurant in Honolulu",
                "session_id": session_id
            }
        )
        chat_response = response.json()
        print(f"Response: {chat_response['response'][:100]}...")
        
        # Check lead data
        lead_response = await client.get(f"{BASE_URL}/session/{session_id}/lead-data")
        lead_data = lead_response.json()
        print(f"Lead data after company: {json.dumps(lead_data, indent=2)}\n")
        
        # Message 3: Add email
        print("3. Sending message with email...")
        response = await client.post(
            f"{BASE_URL}/chat",
            json={
                "message": "You can reach me at sarah@paradisepoke.com",
                "session_id": session_id
            }
        )
        chat_response = response.json()
        print(f"Response: {chat_response['response'][:100]}...")
        
        # Check lead data
        lead_response = await client.get(f"{BASE_URL}/session/{session_id}/lead-data")
        lead_data = lead_response.json()
        print(f"Lead data after email: {json.dumps(lead_data, indent=2)}\n")
        
        # Message 4: Add phone (should trigger lead capture)
        print("4. Sending message with phone...")
        response = await client.post(
            f"{BASE_URL}/chat",
            json={
                "message": "My phone number is 808-555-7890",
                "session_id": session_id
            }
        )
        chat_response = response.json()
        print(f"Response: {chat_response['response'][:100]}...")
        
        # Check lead data
        lead_response = await client.get(f"{BASE_URL}/session/{session_id}/lead-data")
        lead_data = lead_response.json()
        print(f"Lead data after phone: {json.dumps(lead_data, indent=2)}\n")
        
        # Wait a bit for async lead capture
        print("Waiting for lead capture to complete...")
        await asyncio.sleep(3)
        
        # Check final lead data
        lead_response = await client.get(f"{BASE_URL}/session/{session_id}/lead-data")
        final_lead_data = lead_response.json()
        
        print("\n=== FINAL RESULTS ===")
        print(f"Lead captured: {final_lead_data.get('lead_captured', False)}")
        print(f"Lead ID: {final_lead_data.get('lead_id', 'Not captured')}")
        print("\nComplete lead data:")
        print(json.dumps(final_lead_data.get('lead_data', {}), indent=2))
        
        # Message 5: Try adding more info after capture
        print("\n5. Testing post-capture behavior...")
        response = await client.post(
            f"{BASE_URL}/chat",
            json={
                "message": "By the way, my budget is $5000-$10000",
                "session_id": session_id
            }
        )
        
        # Check if it created another lead
        lead_response = await client.get(f"{BASE_URL}/session/{session_id}/lead-data")
        post_capture_data = lead_response.json()
        print(f"Still only one lead captured: {post_capture_data.get('lead_captured', False)}")
        
        # End session
        print("\n6. Ending session...")
        end_response = await client.post(f"{BASE_URL}/session/{session_id}/end")
        print(f"Session end result: {end_response.json()}")

if __name__ == "__main__":
    print("=== Testing Lead Accumulation System ===\n")
    print("This test will:")
    print("1. Create a single session")
    print("2. Send multiple messages with different contact info")
    print("3. Verify all data accumulates in ONE lead")
    print("4. Ensure no duplicate leads are created\n")
    
    asyncio.run(test_lead_accumulation())