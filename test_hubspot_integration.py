#!/usr/bin/env python3
"""
Test HubSpot Integration - Debug why leads aren't appearing in HubSpot
"""
import os
import sys
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

# Setup logging to see all debug info
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Add the api_backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api_backend'))

print("=" * 80)
print("HubSpot Integration Test")
print("=" * 80)

# Check environment variables
print("\n1. Environment Variables Check:")
print("-" * 40)
hubspot_api_key = os.getenv("HUBSPOT_API_KEY")
hubspot_portal_id = os.getenv("HUBSPOT_PORTAL_ID")
hubspot_form_guid = os.getenv("HUBSPOT_FORM_GUID")

print(f"HUBSPOT_API_KEY: {'*' * 10 if hubspot_api_key and hubspot_api_key != 'your_hubspot_api_key_here' else 'NOT CONFIGURED'}")
print(f"HUBSPOT_PORTAL_ID: {hubspot_portal_id if hubspot_portal_id and hubspot_portal_id != 'your_portal_id' else 'NOT CONFIGURED'}")
print(f"HUBSPOT_FORM_GUID: {hubspot_form_guid if hubspot_form_guid else 'NOT CONFIGURED'}")

if hubspot_api_key == "your_hubspot_api_key_here":
    print("\n⚠️  WARNING: HubSpot API key is still set to placeholder value!")
    print("   Please update the HUBSPOT_API_KEY in your .env file with your actual API key")

# Test HubSpot Service directly
print("\n2. Testing HubSpot Service:")
print("-" * 40)

try:
    from services.hubspot_service import HubSpotService
    
    # Create service instance
    hubspot_service = HubSpotService()
    
    print(f"HubSpot Service initialized")
    print(f"API Key configured: {bool(hubspot_service.api_key and hubspot_service.api_key != 'your_hubspot_api_key_here')}")
    print(f"Portal ID: {hubspot_service.portal_id}")
    
    # Test creating a contact if API key is configured
    if hubspot_service.api_key and hubspot_service.api_key != "your_hubspot_api_key_here":
        test_contact_data = {
            "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "first_name": "Test",
            "last_name": "Contact",
            "phone": "808-555-0123",
            "company_name": "Test Hawaiian Business",
            "business_type": "Restaurant",
            "island": "Oahu",
            "primary_challenge": "Need better online presence",
            "budget_range": "$10,000 - $25,000",
            "timeline": "Within 3 months"
        }
        
        print("\nAttempting to create test contact...")
        result = hubspot_service.create_or_update_contact(test_contact_data)
        
        if result.get("success"):
            print(f"✅ Success! Contact created/updated: {result}")
        else:
            print(f"❌ Failed to create contact: {result.get('error')}")
    else:
        print("\n⚠️  Skipping contact creation test - API key not configured")
        
except Exception as e:
    print(f"❌ Error testing HubSpot Service: {str(e)}")
    import traceback
    traceback.print_exc()

# Test Lead Capture Service integration
print("\n3. Testing Lead Capture Service Integration:")
print("-" * 40)

async def test_lead_capture():
    try:
        from services.lead_capture_service import LeadCaptureService
        
        # Create service instance
        lead_service = LeadCaptureService()
        
        print(f"Lead Capture Service initialized")
        print(f"HubSpot API Key configured: {bool(lead_service.hubspot_api_key and lead_service.hubspot_api_key != 'your_hubspot_api_key_here')}")
        
        # Test lead data
        test_lead = {
            "name": "John Doe",
            "email": f"john.doe.{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "phone": "808-555-1234",
            "company": "Aloha Surf Shop",
            "business_type": "Retail - Surf Shop",
            "location": "North Shore, Oahu",
            "main_challenge": "Need to reach more tourists online",
            "budget_range": "$5,000 - $10,000",
            "timeline": "ASAP",
            "values_sustainability": True,
            "local_focus": True,
            "community_minded": True
        }
        
        conversation_summary = "User is interested in AI chatbot for their surf shop to help tourists find the best surf spots and gear."
        
        print("\nCapturing test lead...")
        result = await lead_service.capture_lead(
            lead_data=test_lead,
            conversation_summary=conversation_summary,
            qualification_score=85
        )
        
        print(f"\nLead Capture Result:")
        print(f"  - Success: {result.get('success')}")
        print(f"  - Email sent: {result.get('email_sent')}")
        print(f"  - HubSpot sent: {result.get('hubspot_sent')}")
        print(f"  - Lead ID: {result.get('lead_id')}")
        
        if not result.get('hubspot_sent'):
            print("\n⚠️  Lead was NOT sent to HubSpot!")
            if result.get('error'):
                print(f"   Error: {result.get('error')}")
                
    except Exception as e:
        print(f"❌ Error testing Lead Capture Service: {str(e)}")
        import traceback
        traceback.print_exc()

# Run the async test
asyncio.run(test_lead_capture())

# Check for logged leads
print("\n4. Checking Local Lead Logs:")
print("-" * 40)

leads_dir = "logs/leads"
if os.path.exists(leads_dir):
    lead_files = [f for f in os.listdir(leads_dir) if f.endswith('.json')]
    print(f"Found {len(lead_files)} lead files in {leads_dir}")
    
    # Show most recent 3 leads
    if lead_files:
        lead_files.sort(reverse=True)
        print("\nMost recent leads:")
        for lead_file in lead_files[:3]:
            print(f"  - {lead_file}")
else:
    print(f"❌ Lead logs directory not found: {leads_dir}")

# Summary and recommendations
print("\n" + "=" * 80)
print("SUMMARY AND RECOMMENDATIONS")
print("=" * 80)

if not hubspot_api_key or hubspot_api_key == "your_hubspot_api_key_here":
    print("\n🔴 HubSpot is NOT configured properly!")
    print("\nTo fix this:")
    print("1. Get your HubSpot API key from: https://app.hubspot.com/settings/account/integrations/api-key")
    print("2. Update your .env file:")
    print("   HUBSPOT_API_KEY=your_actual_api_key_here")
    print("3. Optionally add your Portal ID:")
    print("   HUBSPOT_PORTAL_ID=your_portal_id")
    print("4. Restart your application")
else:
    print("\n🟢 HubSpot API key is configured")
    print("\nIf leads still aren't appearing in HubSpot:")
    print("1. Check the API key has proper permissions")
    print("2. Verify the Portal ID is correct")
    print("3. Check HubSpot API logs for errors")
    print("4. Review the application logs for detailed error messages")

print("\n" + "=" * 80)