#!/usr/bin/env python3
"""
Hawaiian Chatbot - Simple Lead Display
Shows all captured leads
"""

import json
from pathlib import Path
from datetime import datetime

def main():
    leads_dir = Path("logs/leads")
    
    if not leads_dir.exists():
        print("❌ No leads directory found!")
        return
    
    lead_files = sorted(leads_dir.glob("lead_*.json"), reverse=True)
    
    print("🌺 Hawaiian Chatbot - Lead Report")
    print("="*80)
    print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Total Leads: {len(lead_files)}")
    print("="*80)
    
    for i, lead_file in enumerate(lead_files):
        try:
            with open(lead_file, 'r') as f:
                lead = json.load(f)
            
            print(f"\n📋 Lead #{i + 1}")
            print("-"*40)
            print(f"ID: {lead.get('lead_id', 'Unknown')}")
            print(f"Date: {lead.get('captured_at', 'Unknown')}")
            print(f"Score: {lead.get('qualification_score', 0)}/100 - {lead.get('lead_quality', 'Unknown')}")
            print(f"\nContact:")
            print(f"  Name: {lead.get('name', '-')}")
            print(f"  Email: {lead.get('email', '-')}")
            print(f"  Phone: {lead.get('phone', '-')}")
            print(f"  Company: {lead.get('company', '-')}")
            print(f"\nBusiness:")
            print(f"  Type: {lead.get('business_type', '-')}")
            print(f"  Location: {lead.get('location', '-')}")
            print(f"  Challenge: {lead.get('main_challenge', '-')}")
            print(f"  Budget: {lead.get('budget_range', '-')}")
            
            if lead.get('conversation_summary'):
                print(f"\nSummary: {lead.get('conversation_summary')}")
                
        except Exception as e:
            print(f"⚠️  Error reading {lead_file}: {e}")
    
    print("\n" + "="*80)
    print("✅ Report complete")
    
    # Quick stats
    hot = sum(1 for f in lead_files if 'HOT' in open(f).read())
    print(f"\n📊 Quick Stats:")
    print(f"  🔥 Hot leads: {hot}")
    print(f"  📧 Total leads: {len(lead_files)}")

if __name__ == "__main__":
    main()