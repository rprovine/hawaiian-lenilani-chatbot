#!/usr/bin/env python3
"""Check and analyze lead files"""
import os
import json
import glob
from datetime import datetime

def check_leads():
    """Check lead files and analyze for duplicates"""
    lead_dir = "logs/leads"
    
    if not os.path.exists(lead_dir):
        print("No leads directory found")
        return
    
    lead_files = sorted(glob.glob(os.path.join(lead_dir, "*.json")))
    
    print(f"Found {len(lead_files)} lead files\n")
    
    # Group leads by contact info to find duplicates
    leads_by_email = {}
    leads_by_phone = {}
    leads_by_name = {}
    
    for lead_file in lead_files:
        try:
            with open(lead_file, 'r') as f:
                lead_data = json.load(f)
                
            # Extract key info
            email = lead_data.get('email')
            phone = lead_data.get('phone')
            name = lead_data.get('name')
            lead_id = lead_data.get('lead_id', os.path.basename(lead_file))
            
            # Group by email
            if email:
                if email not in leads_by_email:
                    leads_by_email[email] = []
                leads_by_email[email].append((lead_id, lead_data))
            
            # Group by phone
            if phone:
                if phone not in leads_by_phone:
                    leads_by_phone[phone] = []
                leads_by_phone[phone].append((lead_id, lead_data))
            
            # Group by name
            if name:
                if name not in leads_by_name:
                    leads_by_name[name] = []
                leads_by_name[name].append((lead_id, lead_data))
                
        except Exception as e:
            print(f"Error reading {lead_file}: {e}")
    
    # Report duplicates
    print("=== DUPLICATE ANALYSIS ===\n")
    
    # Check email duplicates
    print("Duplicate emails:")
    for email, leads in leads_by_email.items():
        if len(leads) > 1:
            print(f"  {email}: {len(leads)} leads")
            for lead_id, data in leads:
                print(f"    - {lead_id}: {data.get('name', 'No name')}, {data.get('captured_at', 'Unknown time')}")
    
    # Check phone duplicates
    print("\nDuplicate phones:")
    for phone, leads in leads_by_phone.items():
        if len(leads) > 1:
            print(f"  {phone}: {len(leads)} leads")
            for lead_id, data in leads:
                print(f"    - {lead_id}: {data.get('name', 'No name')}, {data.get('captured_at', 'Unknown time')}")
    
    # Show recent leads
    print("\n=== RECENT LEADS (Last 5) ===")
    recent_files = sorted(lead_files, key=lambda x: os.path.getmtime(x), reverse=True)[:5]
    
    for lead_file in recent_files:
        try:
            with open(lead_file, 'r') as f:
                lead_data = json.load(f)
            
            print(f"\nLead: {os.path.basename(lead_file)}")
            print(f"  Name: {lead_data.get('name', 'Not provided')}")
            print(f"  Email: {lead_data.get('email', 'Not provided')}")
            print(f"  Phone: {lead_data.get('phone', 'Not provided')}")
            print(f"  Company: {lead_data.get('company', 'Not provided')}")
            print(f"  Captured: {lead_data.get('captured_at', 'Unknown')}")
            
        except Exception as e:
            print(f"Error reading {lead_file}: {e}")

if __name__ == "__main__":
    check_leads()