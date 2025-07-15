#!/usr/bin/env python3
"""
Clear all test leads from the system
Run this in Render Shell to remove all existing leads
"""

import os
import glob
import shutil

print("🌺 Hawaiian Chatbot - Lead Cleanup")
print("="*60)

# Check if leads directory exists
if not os.path.exists('logs/leads'):
    print("❌ No leads directory found")
    exit()

# Count existing leads
lead_files = glob.glob('logs/leads/lead_*.json')
count = len(lead_files)

if count == 0:
    print("✅ No leads to remove")
    exit()

print(f"⚠️  Found {count} lead files")
print("\nThis will DELETE all lead files permanently!")
response = input("\nType 'DELETE ALL' to confirm: ")

if response == "DELETE ALL":
    # Remove all lead files
    removed = 0
    for lead_file in lead_files:
        try:
            os.remove(lead_file)
            removed += 1
            print(f"❌ Deleted: {os.path.basename(lead_file)}")
        except Exception as e:
            print(f"⚠️  Error deleting {lead_file}: {e}")
    
    print(f"\n✅ Removed {removed} lead files")
    
    # Verify empty
    remaining = len(glob.glob('logs/leads/lead_*.json'))
    if remaining == 0:
        print("✅ All leads cleared successfully!")
    else:
        print(f"⚠️  {remaining} files could not be removed")
else:
    print("\n❌ Cancelled - no files were deleted")

print("="*60)