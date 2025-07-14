#!/usr/bin/env python3
"""Final test to verify webhook lead capture is working"""
import requests
import time

def test_webhook_capture():
    url = "http://localhost:8000/chat"
    session_id = "final-webhook-test"
    
    print("🌺 Testing Lead Capture with Webhook")
    print("=" * 50)
    
    messages = [
        "Aloha! I need help with my Poke Bowl restaurant",
        "My name is Keoni Chang, I own Poke Paradise in Honolulu",
        "Email is keoni@pokeparadise.com, phone 808-777-8888",
        "We need inventory tracking and online ordering system",
        "Budget is around $12,000. Ready to start ASAP!",
        "Yes, please schedule consultation this week!"
    ]
    
    for i, msg in enumerate(messages):
        print(f"\n[{i+1}] Sending: {msg}")
        response = requests.post(url, json={"message": msg, "session_id": session_id})
        if response.status_code == 200:
            print(f"✅ Response received")
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("✅ Test complete!")
    print("\n📊 Check these locations:")
    print("1. webhook.site/cc1988a7-e3f8-40e1-9cc1-a5379b53ca1a")
    print("2. logs/leads/ folder for new JSON file")
    print("3. Backend logs show 'Lead sent to webhook successfully'")

if __name__ == "__main__":
    test_webhook_capture()