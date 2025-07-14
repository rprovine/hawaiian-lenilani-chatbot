#!/usr/bin/env python3
"""
Test lead capture functionality
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api_backend'))

from api_backend.services.lead_capture_service import LeadCaptureService

async def test_lead_capture():
    """Test the lead capture service"""
    print("🧪 Testing Lead Capture Service")
    print("=" * 50)
    
    # Check environment variables
    print("\n📋 Environment Check:")
    print(f"SMTP_HOST: {os.getenv('SMTP_HOST', 'NOT SET')}")
    print(f"SMTP_PORT: {os.getenv('SMTP_PORT', 'NOT SET')}")
    print(f"SMTP_USER: {os.getenv('SMTP_USER', 'NOT SET')}")
    print(f"SMTP_PASSWORD: {'SET' if os.getenv('SMTP_PASSWORD') else 'NOT SET'}")
    print(f"LEAD_EMAIL: {os.getenv('LEAD_EMAIL', 'NOT SET')}")
    
    # Initialize service
    try:
        service = LeadCaptureService()
        print("\n✅ Lead Capture Service initialized successfully")
    except Exception as e:
        print(f"\n❌ Failed to initialize service: {e}")
        return
    
    # Test lead data
    test_lead = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "808-555-1234",
        "company": "Test Restaurant",
        "business_type": "Restaurant",
        "location": "Maui",
        "main_challenge": "Inventory management",
        "budget_range": "$5,000-$12,000"
    }
    
    # Test capture
    print("\n📧 Attempting to send test lead...")
    result = await service.capture_lead(
        lead_data=test_lead,
        conversation_summary="Test conversation - Restaurant owner in Maui interested in inventory management system",
        qualification_score=85
    )
    
    print(f"\n📊 Result:")
    print(f"Success: {result['success']}")
    print(f"Email sent: {result.get('email_sent', False)}")
    print(f"HubSpot sent: {result.get('hubspot_sent', False)}")
    if not result['success']:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Check if lead was logged
    lead_id = result.get('lead_id')
    if lead_id:
        log_file = f"logs/leads/{lead_id}.json"
        if os.path.exists(log_file):
            print(f"\n✅ Lead logged successfully to: {log_file}")
        else:
            print(f"\n❌ Lead log file not found: {log_file}")

if __name__ == "__main__":
    print("🌺 Hawaiian LeniLani Lead Capture Test")
    print("=" * 50)
    asyncio.run(test_lead_capture())