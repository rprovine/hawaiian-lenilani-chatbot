#!/usr/bin/env python3
"""
Quick HubSpot verification script
Run this in Render Shell to check HubSpot configuration
"""

import os
import requests
import json
from datetime import datetime

print("🌺 HubSpot Integration Checker")
print("="*60)

# Check environment variables
api_key = os.getenv("HUBSPOT_API_KEY", "")
portal_id = os.getenv("HUBSPOT_PORTAL_ID", "")

print("\n1️⃣ Environment Variables:")
print(f"   HUBSPOT_API_KEY: {'✅ Set' if api_key and api_key != 'your_hubspot_api_key_here' else '❌ Not set or placeholder'}")
print(f"   Key format: {'✅ Valid (pat-)' if api_key.startswith('pat-') else '❌ Invalid format'}")
print(f"   HUBSPOT_PORTAL_ID: {'✅ Set' if portal_id and portal_id != 'your_portal_id' else '❌ Not set or placeholder'}")

if not api_key or api_key == "your_hubspot_api_key_here":
    print("\n❌ ERROR: HubSpot API key not configured!")
    print("\nTo fix:")
    print("1. Go to Render Dashboard → Environment")
    print("2. Add: HUBSPOT_API_KEY = pat-na1-your-actual-key")
    print("3. Add: HUBSPOT_PORTAL_ID = your-portal-id")
    exit(1)

# Test API connection
print("\n2️⃣ Testing API Connection...")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    # Test with account info endpoint
    response = requests.get(
        "https://api.hubapi.com/account-info/v3/details",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ API connection successful!")
        account = response.json()
        print(f"   Portal ID: {account.get('portalId')}")
        print(f"   Time Zone: {account.get('timeZone')}")
    else:
        print(f"❌ API error: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Connection error: {e}")

# Test creating a contact
print("\n3️⃣ Testing Contact Creation...")
test_contact = {
    "properties": {
        "email": f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
        "firstname": "Test",
        "lastname": "Lead",
        "company": "Test Company",
        "phone": "808-555-0000",
        "hs_lead_status": "NEW",
        "island_location": "Oahu",
        "business_type_hawaii": "Test Business",
        "lead_source": "Hawaiian AI Chatbot Test"
    }
}

try:
    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/contacts",
        headers=headers,
        json=test_contact
    )
    
    if response.status_code == 201:
        contact = response.json()
        print("✅ Test contact created successfully!")
        print(f"   Contact ID: {contact.get('id')}")
        print(f"   Test email: {test_contact['properties']['email']}")
        print("\n✅ HubSpot integration is working!")
    else:
        print(f"❌ Failed to create contact: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error creating contact: {e}")

# Check recent leads
print("\n4️⃣ Checking Recent Leads...")
try:
    # Check local lead files
    import glob
    lead_files = sorted(glob.glob('logs/leads/*.json'), reverse=True)[:5]
    
    if lead_files:
        print(f"   Found {len(lead_files)} recent local leads")
        
        # Check the most recent lead
        with open(lead_files[0]) as f:
            recent_lead = json.load(f)
        
        print(f"   Most recent: {recent_lead.get('email', 'No email')}")
        print(f"   Captured: {recent_lead.get('captured_at', 'Unknown')}")
        
        # Check if this lead exists in HubSpot
        if recent_lead.get('email'):
            search_response = requests.get(
                f"https://api.hubapi.com/crm/v3/objects/contacts/{recent_lead['email']}?idProperty=email",
                headers=headers
            )
            
            if search_response.status_code == 200:
                print(f"   ✅ Lead found in HubSpot!")
            else:
                print(f"   ❌ Lead NOT found in HubSpot")
    else:
        print("   No local leads found")
        
except Exception as e:
    print(f"   Error checking leads: {e}")

print("\n" + "="*60)
print("✅ Test complete!")
print("\nIf leads aren't syncing:")
print("1. Check that HUBSPOT_API_KEY is set correctly in Render")
print("2. Make sure the API key has contact read/write permissions")
print("3. Check Render logs for any HubSpot errors")
print("4. Ensure the deployment has completed")