#!/usr/bin/env python3
"""Test full lead capture flow"""
import asyncio
import logging
from api_backend.services.hawaiian_conversation_router import HawaiianConversationRouter
from api_backend.services.lead_capture_service import LeadCaptureService

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_full_lead_capture():
    # Create services
    router = HawaiianConversationRouter()
    lead_service = LeadCaptureService()
    
    # Test lead data
    test_lead = {
        "name": "Sarah Kim",
        "email": "sarah@kahikomarket.com",
        "phone": "808-555-7777",
        "company": "Kahiko Market",
        "business_type": "Retail",
        "location": "Oahu",
        "main_challenge": "Inventory management across multiple locations",
        "budget_range": "$10,000-$20,000",
        "message_count": 5
    }
    
    # Test capture
    print("Testing lead capture...")
    result = await lead_service.capture_lead(
        lead_data=test_lead,
        conversation_summary="Retail owner needs multi-location inventory system",
        qualification_score=75
    )
    
    print(f"Lead capture result: {result}")
    
    # Check if webhook was sent
    if result.get("success"):
        print("✅ Lead captured successfully!")
        print(f"  - Email sent: {result.get('email_sent', False)}")
        print(f"  - HubSpot sent: {result.get('hubspot_sent', False)}")
        print(f"  - Lead ID: {result.get('lead_id')}")
    else:
        print("❌ Lead capture failed!")
        print(f"  - Error: {result.get('error')}")

if __name__ == "__main__":
    asyncio.run(test_full_lead_capture())