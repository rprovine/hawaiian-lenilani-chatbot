#!/usr/bin/env python3
"""Direct test of webhook sending"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_webhook_direct():
    from api_backend.services.webhook_lead_capture import WebhookLeadCapture, create_zapier_friendly_lead
    
    # Create test lead
    test_lead = {
        "lead_id": "lead_test_direct",
        "name": "John Doe",
        "email": "john@testrestaurant.com", 
        "phone": "808-555-9999",
        "company": "Test Restaurant",
        "business_type": "Restaurant",
        "location": "Maui",
        "main_challenge": "Online ordering crashes",
        "budget_range": "$5,000-$10,000",
        "qualification_score": 85,
        "lead_quality": "🔥 HOT - Ready to buy",
        "conversation_summary": "Restaurant owner needs reliable online ordering system"
    }
    
    # Test webhook
    webhook_service = WebhookLeadCapture()
    print(f"Webhook URL configured: {webhook_service.webhook_url}")
    
    if webhook_service.webhook_url:
        zapier_lead = create_zapier_friendly_lead(test_lead)
        result = await webhook_service.send_lead(zapier_lead)
        print(f"Webhook result: {result}")
    else:
        print("No webhook URL configured in .env")

if __name__ == "__main__":
    asyncio.run(test_webhook_direct())