#!/usr/bin/env python3
"""
Hawaiian Chatbot - Lead Viewer
Shows all captured leads with details
"""

import json
import os
from datetime import datetime
from pathlib import Path
import pytz

def load_leads():
    """Load all lead files from logs directory"""
    leads_dir = Path("logs/leads")
    leads = []
    
    if not leads_dir.exists():
        print("❌ No leads directory found at logs/leads/")
        return leads
    
    # Get all JSON files
    lead_files = sorted(leads_dir.glob("lead_*.json"), reverse=True)
    
    for lead_file in lead_files:
        try:
            with open(lead_file, 'r') as f:
                lead = json.load(f)
                leads.append(lead)
        except Exception as e:
            print(f"⚠️  Error reading {lead_file}: {e}")
    
    return leads

def display_lead(lead, index):
    """Display a single lead with formatting"""
    print(f"\n{'='*60}")
    print(f"📋 Lead #{index + 1}")
    print(f"{'='*60}")
    
    # Basic info
    print(f"🆔 ID: {lead.get('lead_id', 'Unknown')}")
    print(f"📅 Captured: {lead.get('captured_at', 'Unknown')}")
    print(f"⭐ Score: {lead.get('qualification_score', 0)}/100")
    print(f"🔥 Quality: {lead.get('lead_quality', 'Unknown')}")
    
    # Contact info
    print(f"\n👤 Contact Information:")
    print(f"   Name: {lead.get('name', 'Not provided')}")
    print(f"   Email: {lead.get('email', 'Not provided')}")
    print(f"   Phone: {lead.get('phone', 'Not provided')}")
    print(f"   Company: {lead.get('company', 'Not provided')}")
    
    # Business info
    print(f"\n🏢 Business Details:")
    print(f"   Type: {lead.get('business_type', 'Not provided')}")
    print(f"   Location: {lead.get('location', 'Not provided')}")
    print(f"   Challenge: {lead.get('main_challenge', 'Not provided')}")
    print(f"   Budget: {lead.get('budget_range', 'Not provided')}")
    
    # Summary
    if lead.get('conversation_summary'):
        print(f"\n💬 Summary: {lead.get('conversation_summary')}")

def generate_summary(leads):
    """Generate summary statistics"""
    if not leads:
        return
    
    print(f"\n\n{'='*60}")
    print(f"📊 LEAD SUMMARY")
    print(f"{'='*60}")
    
    # Total leads
    print(f"📈 Total Leads: {len(leads)}")
    
    # Quality breakdown
    hot_leads = sum(1 for l in leads if 'HOT' in l.get('lead_quality', ''))
    warm_leads = sum(1 for l in leads if 'WARM' in l.get('lead_quality', ''))
    cold_leads = sum(1 for l in leads if 'COLD' in l.get('lead_quality', ''))
    
    print(f"\n🎯 Lead Quality:")
    print(f"   🔥 Hot: {hot_leads}")
    print(f"   🌡️  Warm: {warm_leads}")
    print(f"   ❄️  Cold: {cold_leads}")
    
    # Average score
    scores = [l.get('qualification_score', 0) for l in leads]
    avg_score = sum(scores) / len(scores) if scores else 0
    print(f"\n⭐ Average Score: {avg_score:.1f}/100")
    
    # Location breakdown
    locations = {}
    for lead in leads:
        loc = lead.get('location', 'Unknown')
        locations[loc] = locations.get(loc, 0) + 1
    
    print(f"\n🏝️  Locations:")
    for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
        print(f"   {loc}: {count}")
    
    # Business types
    types = {}
    for lead in leads:
        btype = lead.get('business_type', 'Unknown')
        types[btype] = types.get(btype, 0) + 1
    
    print(f"\n🏢 Business Types:")
    for btype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"   {btype}: {count}")

def export_to_csv(leads):
    """Export leads to CSV file"""
    import csv
    
    if not leads:
        return
    
    filename = f"leads_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['lead_id', 'captured_at', 'name', 'email', 'phone', 
                     'company', 'business_type', 'location', 'main_challenge',
                     'budget_range', 'qualification_score', 'lead_quality', 
                     'conversation_summary']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for lead in leads:
            writer.writerow({k: lead.get(k, '') for k in fieldnames})
    
    print(f"\n✅ Exported {len(leads)} leads to {filename}")

def main():
    """Main function"""
    print("🌺 Hawaiian Chatbot - Lead Viewer")
    print("="*60)
    
    # Load leads
    leads = load_leads()
    
    if not leads:
        print("\n❌ No leads found!")
        print("\n💡 Leads are captured when users provide:")
        print("   - Email address")
        print("   - Phone number")
        print("   - Business information")
        return
    
    print(f"\n✅ Found {len(leads)} leads")
    
    # Display options
    while True:
        print("\n" + "="*60)
        print("📋 OPTIONS:")
        print("1. View all leads")
        print("2. View summary only")
        print("3. Export to CSV")
        print("4. View specific lead")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            for i, lead in enumerate(leads):
                display_lead(lead, i)
            generate_summary(leads)
            
        elif choice == '2':
            generate_summary(leads)
            
        elif choice == '3':
            export_to_csv(leads)
            
        elif choice == '4':
            try:
                lead_num = int(input(f"Enter lead number (1-{len(leads)}): ")) - 1
                if 0 <= lead_num < len(leads):
                    display_lead(leads[lead_num], lead_num)
                else:
                    print("❌ Invalid lead number")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == '5':
            print("\n🌺 Aloha! Mahalo for using Lead Viewer!")
            break
            
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()