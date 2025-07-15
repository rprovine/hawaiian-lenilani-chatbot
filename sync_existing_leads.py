#!/usr/bin/env python3
"""
Sync existing leads from logs/leads/ to HubSpot
Run this after deploying the HubSpot fix
"""

import os
import sys
import json
import glob
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_backend.services.hubspot_service import hubspot_service


def sync_existing_leads():
    """Sync all existing leads to HubSpot"""
    
    print("🌺 Syncing Existing Leads to HubSpot")
    print("=" * 60)
    
    # Check if HubSpot is configured
    if not hubspot_service.api_key or hubspot_service.api_key == "your_hubspot_api_key_here":
        print("❌ ERROR: HubSpot API key not configured!")
        print("Please set HUBSPOT_API_KEY in your .env file or Render environment")
        return
    
    # Find all lead files
    lead_files = sorted(glob.glob('logs/leads/*.json'))
    
    if not lead_files:
        print("No leads found in logs/leads/")
        return
    
    print(f"\nFound {len(lead_files)} leads to sync")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, lead_file in enumerate(lead_files, 1):
        try:
            # Load lead data
            with open(lead_file, 'r') as f:
                lead_data = json.load(f)
            
            email = lead_data.get('email', '')
            name = lead_data.get('name', 'Unknown')
            
            print(f"\n{i}/{len(lead_files)}: Processing {name} ({email})")
            
            # Skip if no email
            if not email:
                print("   ⚠️  Skipped - No email address")
                skip_count += 1
                continue
            
            # Prepare contact data for HubSpot
            contact_data = {
                "email": email,
                "first_name": name.split()[0] if name else "",
                "last_name": " ".join(name.split()[1:]) if name and len(name.split()) > 1 else "",
                "phone": lead_data.get("phone"),
                "company_name": lead_data.get("company"),
                "business_type": lead_data.get("business_type"),
                "island": lead_data.get("location"),
                "primary_challenge": lead_data.get("main_challenge"),
                "budget_range": lead_data.get("budget_range"),
                "timeline": lead_data.get("timeline", "Not specified"),
                "values_sustainability": lead_data.get("values_sustainability", False),
                "local_focus": lead_data.get("local_focus", True),
                "community_minded": lead_data.get("community_minded", True),
            }
            
            # Create or update contact
            result = hubspot_service.create_or_update_contact(contact_data)
            
            if result.get("success"):
                print(f"   ✅ Success - {result.get('action', 'processed')} (ID: {result.get('contact_id')})")
                success_count += 1
                
                # For high-scoring leads, create deals
                if lead_data.get("qualification_score", 0) >= 70:
                    print("   📊 Creating deal for high-scoring lead...")
                    deal_data = {
                        "company_name": lead_data.get("company", "Hawaiian Business"),
                        "services": ["AI Chatbot", "Consulting"],
                        "timeline": lead_data.get("timeline", "Not specified"),
                        "island": lead_data.get("location"),
                        "business_type": lead_data.get("business_type"),
                        "primary_service": "AI Solutions"
                    }
                    
                    deal_result = hubspot_service.create_deal(
                        result.get("contact_id"),
                        deal_data
                    )
                    
                    if deal_result.get("success"):
                        print(f"   💰 Deal created (ID: {deal_result.get('deal_id')})")
            else:
                print(f"   ❌ Failed - {result.get('error', 'Unknown error')}")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ Error - {str(e)}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Sync Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ⚠️  Skipped: {skip_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📁 Total: {len(lead_files)}")
    
    if success_count > 0:
        print("\n✨ Leads synced to HubSpot successfully!")
        print("Check your HubSpot contacts at: https://app.hubspot.com/contacts")


if __name__ == "__main__":
    sync_existing_leads()