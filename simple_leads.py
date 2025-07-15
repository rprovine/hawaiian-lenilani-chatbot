import os
import json
import glob

# Create directories if needed
os.makedirs('logs/leads', exist_ok=True)

# Find all lead files
files = glob.glob('logs/leads/*.json')

print("Total leads:", len(files))

# Show each lead
for i, filename in enumerate(files):
    print(f"\n--- Lead {i+1} ---")
    try:
        with open(filename) as f:
            lead = json.load(f)
        print("Email:", lead.get('email', 'N/A'))
        print("Phone:", lead.get('phone', 'N/A'))
        print("Name:", lead.get('name', 'N/A'))
        print("Score:", lead.get('qualification_score', 'N/A'))
    except:
        print("Error reading file")