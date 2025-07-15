#!/usr/bin/env python3
"""
Quick lead viewer - paste this into Render Shell
"""

import json
import glob
import os
from datetime import datetime

print("\n🌺 Hawaiian Chatbot - Lead Report")
print("="*60)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Check if leads directory exists
if not os.path.exists('logs/leads'):
    print("\n❌ ERROR: logs/leads directory not found!")
    print("\nCreating directories...")
    os.makedirs('logs/leads', exist_ok=True)
    print("✅ Directories created. No leads yet.")
else:
    # Get all lead files
    lead_files = sorted(glob.glob('logs/leads/lead_*.json'))
    
    if not lead_files:
        print("\n❌ No lead files found in logs/leads/")
        print("\nMake sure:")
        print("1. Users have provided contact info in chat")
        print("2. Lead capture is working properly")
    else:
        print(f"\n✅ Found {len(lead_files)} leads\n")
        
        # Process each lead
        hot_count = 0
        warm_count = 0
        cold_count = 0
        
        for i, lead_file in enumerate(lead_files):
            try:
                with open(lead_file, 'r') as f:
                    lead = json.load(f)
                
                print(f"📋 Lead #{i+1}")
                print("-"*40)
                print(f"Date: {lead.get('captured_at', 'Unknown')}")
                print(f"Score: {lead.get('qualification_score', 0)}/100")
                print(f"Quality: {lead.get('lead_quality', 'Unknown')}")
                
                # Contact info
                if lead.get('name') or lead.get('email') or lead.get('phone'):
                    print("\nContact:")
                    if lead.get('name'): print(f"  Name: {lead['name']}")
                    if lead.get('email'): print(f"  Email: {lead['email']}")
                    if lead.get('phone'): print(f"  Phone: {lead['phone']}")
                    if lead.get('company'): print(f"  Company: {lead['company']}")
                
                # Business info
                if lead.get('business_type') or lead.get('location'):
                    print("\nBusiness:")
                    if lead.get('business_type'): print(f"  Type: {lead['business_type']}")
                    if lead.get('location'): print(f"  Location: {lead['location']}")
                    if lead.get('main_challenge'): print(f"  Challenge: {lead['main_challenge']}")
                    if lead.get('budget_range'): print(f"  Budget: {lead['budget_range']}")
                
                if lead.get('conversation_summary'):
                    print(f"\nSummary: {lead['conversation_summary'][:100]}...")
                
                print()
                
                # Count quality
                quality = lead.get('lead_quality', '')
                if 'HOT' in quality: hot_count += 1
                elif 'WARM' in quality: warm_count += 1
                else: cold_count += 1
                
            except Exception as e:
                print(f"Error reading {lead_file}: {e}")
        
        # Summary
        print("="*60)
        print("📊 SUMMARY")
        print("="*60)
        print(f"Total Leads: {len(lead_files)}")
        print(f"🔥 Hot: {hot_count}")
        print(f"🌡️  Warm: {warm_count}")
        print(f"❄️  Cold: {cold_count}")

print("\n✅ Report complete!")