#!/usr/bin/env python3
"""
Simple lead sync script for Render shell
Copy and paste this into the Render shell after deployment
"""

import os
import json
import glob

# Make sure we're in the right directory
os.chdir('/app')

# Import the hubspot service
from api_backend.services.hubspot_service import hubspot_service

# Find lead files
lead_files = sorted(glob.glob('logs/leads/*.json'))
print(f"Found {len(lead_files)} leads")

success = 0
for lead_file in lead_files:
    try:
        with open(lead_file) as f:
            lead = json.load(f)
        
        if not lead.get('email'):
            continue
            
        # Sync to HubSpot
        contact_data = {
            "email": lead.get("email"),
            "first_name": lead.get("name", "").split()[0] if lead.get("name") else "",
            "last_name": " ".join(lead.get("name", "").split()[1:]) if lead.get("name") and len(lead.get("name", "").split()) > 1 else "",
            "phone": lead.get("phone"),
            "company_name": lead.get("company"),
            "business_type": lead.get("business_type"),
            "island": lead.get("location"),
            "primary_challenge": lead.get("main_challenge"),
            "budget_range": lead.get("budget_range"),
        }
        
        result = hubspot_service.create_or_update_contact(contact_data)
        if result.get("success"):
            print(f"✅ Synced: {lead.get('email')}")
            success += 1
        else:
            print(f"❌ Failed: {lead.get('email')} - {result.get('error')}")
            
    except Exception as e:
        print(f"Error: {e}")

print(f"\nSynced {success}/{len(lead_files)} leads to HubSpot")