#!/usr/bin/env python3
"""
View leads from downloaded JSON file
Usage: python view_leads_from_file.py server_leads.json
"""

import json
import sys
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: python view_leads_from_file.py <json_file>")
    sys.exit(1)

try:
    with open(sys.argv[1], 'r') as f:
        leads = json.load(f)
    
    print(f"\n🌺 Lead Report - {len(leads)} Total Leads")
    print("="*80)
    
    for i, lead in enumerate(leads):
        print(f"\n📋 Lead #{i+1}")
        print("-"*40)
        print(f"ID: {lead.get('lead_id', 'Unknown')}")
        print(f"Date: {lead.get('captured_at', 'Unknown')}")
        print(f"Score: {lead.get('qualification_score', 0)}/100")
        print(f"Quality: {lead.get('lead_quality', 'Unknown')}")
        
        print(f"\nContact:")
        print(f"  Name: {lead.get('name') or '-'}")
        print(f"  Email: {lead.get('email') or '-'}")
        print(f"  Phone: {lead.get('phone') or '-'}")
        print(f"  Company: {lead.get('company') or '-'}")
        
        print(f"\nBusiness:")
        print(f"  Type: {lead.get('business_type') or '-'}")
        print(f"  Location: {lead.get('location') or '-'}")
        print(f"  Challenge: {lead.get('main_challenge') or '-'}")
        print(f"  Budget: {lead.get('budget_range') or '-'}")
        
        if lead.get('conversation_summary'):
            print(f"\nSummary: {lead.get('conversation_summary')}")
    
    # Summary stats
    hot = sum(1 for l in leads if 'HOT' in l.get('lead_quality', ''))
    warm = sum(1 for l in leads if 'WARM' in l.get('lead_quality', ''))
    cold = sum(1 for l in leads if 'COLD' in l.get('lead_quality', ''))
    
    print(f"\n{'='*80}")
    print(f"📊 Summary:")
    print(f"  Total: {len(leads)}")
    print(f"  🔥 Hot: {hot}")
    print(f"  🌡️  Warm: {warm}")
    print(f"  ❄️  Cold: {cold}")
    
except FileNotFoundError:
    print(f"Error: File '{sys.argv[1]}' not found")
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in '{sys.argv[1]}'")
except Exception as e:
    print(f"Error: {e}")
