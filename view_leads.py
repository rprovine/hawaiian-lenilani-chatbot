#!/usr/bin/env python3
import json
import os
from datetime import datetime

def display_leads():
      leads_dir = "logs/leads"

      print("\n" + "="*70)
      print("                    🌺 LENILANI CAPTURED LEADS 🌺")
      print("="*70 + "\n")

      if not os.path.exists(leads_dir):
          print("No leads directory found!")
          return

      lead_files = sorted([f for f in os.listdir(leads_dir) if f.endswith('.json')])

      if not lead_files:
          print("No leads captured yet.")
          return

      for i, filename in enumerate(lead_files, 1):
          with open(os.path.join(leads_dir, filename), 'r') as f:
              lead = json.load(f)

          print(f"Lead #{i}")
          print("-" * 50)
          print(f"📧 Email:    {lead.get('email', 'Not provided')}")
          print(f"👤 Name:     {lead.get('name', 'Not provided')}")
          print(f"📱 Phone:    {lead.get('phone', 'Not provided')}")
          print(f"🏢 Business: {lead.get('business_type', 'Not specified')}")
          print(f"🏝️  Location: {lead.get('location', 'Not specified')}")
          print(f"⭐ Score:    {lead.get('qualification_score', 0)}/100 - {lead.get('lead_quality', 'Unknown')}")
          print(f"💬 Messages: {lead.get('message_count', 0)} exchanged")
          print(f"📝 Summary:  {lead.get('conversation_summary', 'No summary')}")

          captured_at = lead.get('captured_at', '')
          if captured_at:
              try:
                  dt = datetime.fromisoformat(captured_at.replace('Z', '+00:00'))
                  formatted_time = dt.strftime('%B %d, %Y at %I:%M %p')
                  print(f"📅 Captured: {formatted_time}")
              except:
                  print(f"📅 Captured: {captured_at}")

          print("\n")

      print(f"Total leads captured: {len(lead_files)}")
      print("="*70 + "\n")

if __name__ == "__main__":
    display_leads()
