#!/usr/bin/env python3
"""
Initialize required directories for the application
This should be run before starting the app on a new server
"""
import os
import sys


def create_directories():
    """Create all required directories"""
    directories = [
        "logs",
        "logs/leads",
    ]
    
    print("📁 Creating required directories...\n")
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            if os.path.exists(directory):
                print(f"✅ {directory}/ - Created/Verified")
            else:
                print(f"❌ {directory}/ - Failed to create")
                return False
        except Exception as e:
            print(f"❌ {directory}/ - Error: {str(e)}")
            return False
    
    print("\n✅ All directories created successfully!")
    return True


if __name__ == "__main__":
    success = create_directories()
    sys.exit(0 if success else 1)