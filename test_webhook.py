#!/usr/bin/env python3
"""Test webhook lead capture"""
import requests
import json

def test_webhook():
    url = "http://localhost:8000/chat"
    
    # Test conversation with lead info
    messages = [
        {
            "message": "I need help with my restaurant's online ordering system. My email is john@mauigrindz.com and phone is 808-555-8888",
            "session_id": "webhook-test-2"
        },
        {
            "message": "We're located in Kihei, Maui. Main issue is our current system crashes during peak hours",
            "session_id": "webhook-test-2"
        },
        {
            "message": "Our budget is around $5,000-10,000. We need something reliable that can handle 50+ orders per hour",
            "session_id": "webhook-test-2"
        },
        {
            "message": "Yes, let's schedule a consultation! This is urgent for us",
            "session_id": "webhook-test-2"
        }
    ]
    
    for msg in messages:
        print(f"\nSending: {msg['message']}")
        try:
            response = requests.post(url, json=msg)
            print(f"Response: {response.json().get('response', 'No response')[:200]}...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_webhook()