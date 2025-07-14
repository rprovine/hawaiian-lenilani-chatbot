#!/usr/bin/env python3
"""Test lead capture through chat API"""
import requests
import time

def test_chat_lead_capture():
    url = "http://localhost:8000/chat"
    session_id = "lead-test-final"
    
    # Conversation that should trigger lead capture
    messages = [
        "Aloha! I run a clothing boutique in Lahaina and need help with inventory tracking",
        "My name is Mike Tanaka, email is mike@lahainalooks.com",  
        "Phone is 808-661-5555. We have 3 locations on Maui",
        "Main challenge is tracking inventory across all stores in real-time",
        "Budget is flexible, probably $15,000-25,000 range",
        "Yes I'd like to schedule a consultation this week if possible!"
    ]
    
    print("Testing lead capture through chat API...")
    print("=" * 50)
    
    for i, msg in enumerate(messages):
        print(f"\n[{i+1}] Sending: {msg}")
        
        try:
            response = requests.post(url, json={
                "message": msg,
                "session_id": session_id
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {data.get('response', '')[:150]}...")
            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(1)  # Small delay between messages
    
    print("\n" + "=" * 50)
    print("✅ Test complete! Check:")
    print("  1. webhook.site dashboard for incoming lead")
    print("  2. logs/leads/ folder for new JSON file")
    print("  3. Backend console for lead capture logs")

if __name__ == "__main__":
    test_chat_lead_capture()