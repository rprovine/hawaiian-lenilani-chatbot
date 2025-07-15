#!/usr/bin/env python3
"""
HubSpot Setup Helper - Guide for configuring HubSpot integration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 80)
print("🌺 Hawaiian LeniLani Chatbot - HubSpot Setup Guide")
print("=" * 80)

# Check current configuration
hubspot_api_key = os.getenv("HUBSPOT_API_KEY")
hubspot_portal_id = os.getenv("HUBSPOT_PORTAL_ID")
hubspot_form_guid = os.getenv("HUBSPOT_FORM_GUID")

print("\n📋 Current Configuration:")
print("-" * 40)

if hubspot_api_key == "your_hubspot_api_key_here":
    print("❌ HUBSPOT_API_KEY: Not configured (still placeholder)")
elif hubspot_api_key:
    print(f"✅ HUBSPOT_API_KEY: {'*' * 10} (configured)")
else:
    print("❌ HUBSPOT_API_KEY: Not set")

if hubspot_portal_id == "your_portal_id":
    print("❌ HUBSPOT_PORTAL_ID: Not configured (still placeholder)")
elif hubspot_portal_id:
    print(f"✅ HUBSPOT_PORTAL_ID: {hubspot_portal_id}")
else:
    print("❌ HUBSPOT_PORTAL_ID: Not set")

if hubspot_form_guid:
    print(f"ℹ️  HUBSPOT_FORM_GUID: {hubspot_form_guid}")
else:
    print("ℹ️  HUBSPOT_FORM_GUID: Not set (optional)")

print("\n🔧 Setup Instructions:")
print("-" * 40)

if not hubspot_api_key or hubspot_api_key == "your_hubspot_api_key_here":
    print("\n1. Get your HubSpot API Key:")
    print("   a. Log in to HubSpot: https://app.hubspot.com")
    print("   b. Go to Settings (gear icon)")
    print("   c. Navigate to: Integrations > API Key")
    print("   d. Generate a new API key if you don't have one")
    print("   e. Copy the API key")
    
    print("\n2. Update your .env file:")
    print("   Open .env and replace:")
    print("   HUBSPOT_API_KEY=your_hubspot_api_key_here")
    print("   With:")
    print("   HUBSPOT_API_KEY=<your-actual-api-key>")

if not hubspot_portal_id or hubspot_portal_id == "your_portal_id":
    print("\n3. Get your Portal ID (Account ID):")
    print("   a. In HubSpot, click your account name (top right)")
    print("   b. Your Portal ID is the number shown")
    print("   c. Update .env file:")
    print("   HUBSPOT_PORTAL_ID=<your-portal-id>")

print("\n4. Create Custom Properties (Optional but Recommended):")
print("   In HubSpot, go to Settings > Properties > Contact Properties")
print("   Create these custom properties:")
print("   - island_location (Single-line text)")
print("   - business_type_hawaii (Single-line text)")
print("   - primary_challenge (Multi-line text)")
print("   - budget_range (Single-line text)")
print("   - timeline (Single-line text)")
print("   - lead_score (Number)")
print("   - cultural_alignment (Single-line text)")

print("\n5. Test the Integration:")
print("   Run: python test_hubspot_integration.py")

print("\n📝 Example .env configuration:")
print("-" * 40)
print("""
# HubSpot Integration
HUBSPOT_API_KEY=pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
HUBSPOT_PORTAL_ID=12345678
# HUBSPOT_FORM_GUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # Optional
""")

print("\n⚡ Quick Test Commands:")
print("-" * 40)
print("1. Test HubSpot connection:")
print("   python test_hubspot_integration.py")
print("\n2. Test full lead capture flow:")
print("   python test_full_lead_capture.py")
print("\n3. View captured leads:")
print("   python show_leads.py")

print("\n🔒 Security Notes:")
print("-" * 40)
print("- Never commit your .env file to git")
print("- Keep your API key secure")
print("- Use environment variables in production")
print("- Consider using HubSpot Private Apps for better security")

print("\n" + "=" * 80)