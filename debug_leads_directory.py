#!/usr/bin/env python3
"""
Debug script to check leads directory on the server
Run this in the Render shell to diagnose issues
"""
import os
import sys
import json
from pathlib import Path


def check_directory_status():
    """Check the status of various directories"""
    print("🔍 Checking directory status...\n")
    
    # Check current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    
    # Check if logs directory exists
    logs_exists = os.path.exists("logs")
    print(f"logs/ directory exists: {logs_exists}")
    
    if logs_exists:
        # Check permissions
        logs_stat = os.stat("logs")
        print(f"logs/ permissions: {oct(logs_stat.st_mode)}")
        
        # List contents
        logs_contents = os.listdir("logs")
        print(f"logs/ contents: {logs_contents}")
    
    # Check if logs/leads directory exists
    leads_dir = "logs/leads"
    leads_exists = os.path.exists(leads_dir)
    print(f"\nlogs/leads/ directory exists: {leads_exists}")
    
    if leads_exists:
        # Check permissions
        leads_stat = os.stat(leads_dir)
        print(f"logs/leads/ permissions: {oct(leads_stat.st_mode)}")
        
        # List contents
        leads_contents = os.listdir(leads_dir)
        print(f"Number of lead files: {len(leads_contents)}")
        
        if leads_contents:
            print("\nRecent lead files:")
            for file in sorted(leads_contents)[-5:]:  # Show last 5
                file_path = os.path.join(leads_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"  - {file} ({file_size} bytes)")


def try_create_directories():
    """Try to create the directories"""
    print("\n🔨 Attempting to create directories...\n")
    
    try:
        # Try to create logs directory
        os.makedirs("logs", exist_ok=True)
        print("✅ Created/verified logs/ directory")
        
        # Try to create logs/leads directory
        os.makedirs("logs/leads", exist_ok=True)
        print("✅ Created/verified logs/leads/ directory")
        
        # Verify they exist
        if os.path.exists("logs/leads"):
            print("✅ Confirmed logs/leads/ directory exists")
        else:
            print("❌ logs/leads/ directory does not exist after creation")
            
    except Exception as e:
        print(f"❌ Error creating directories: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        
        # Try to get more info
        try:
            import traceback
            traceback.print_exc()
        except:
            pass


def test_write_lead():
    """Test writing a lead file"""
    print("\n📝 Testing lead file write...\n")
    
    test_lead = {
        "lead_id": "test_debug_lead",
        "name": "Debug Test",
        "email": "debug@test.com",
        "timestamp": "2025-01-15T12:00:00"
    }
    
    try:
        # Ensure directory exists
        os.makedirs("logs/leads", exist_ok=True)
        
        # Write test file
        test_file = "logs/leads/test_debug_lead.json"
        with open(test_file, 'w') as f:
            json.dump(test_lead, f, indent=2)
        
        print(f"✅ Successfully wrote test file: {test_file}")
        
        # Verify it exists
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"✅ Confirmed file exists, size: {file_size} bytes")
            
            # Read it back
            with open(test_file, 'r') as f:
                content = json.load(f)
            print(f"✅ Successfully read file back: {content.get('name')}")
        else:
            print("❌ Test file does not exist after write")
            
    except Exception as e:
        print(f"❌ Error writing test lead: {str(e)}")
        print(f"   Error type: {type(e).__name__}")


def check_environment():
    """Check environment details"""
    print("\n🌍 Environment Information:\n")
    
    # Python version
    print(f"Python version: {sys.version}")
    
    # User info
    try:
        import pwd
        user_info = pwd.getpwuid(os.getuid())
        print(f"Running as user: {user_info.pw_name} (UID: {os.getuid()})")
    except:
        print(f"UID: {os.getuid()}")
    
    # Working directory permissions
    cwd_stat = os.stat(".")
    print(f"Working directory permissions: {oct(cwd_stat.st_mode)}")
    
    # Check if we can write to current directory
    try:
        test_file = ".write_test"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✅ Can write to current directory")
    except:
        print("❌ Cannot write to current directory")


if __name__ == "__main__":
    print("🔍 Lead Directory Debug Script\n")
    print("=" * 50)
    
    check_environment()
    print("\n" + "=" * 50)
    
    check_directory_status()
    print("\n" + "=" * 50)
    
    try_create_directories()
    print("\n" + "=" * 50)
    
    test_write_lead()
    print("\n" + "=" * 50)
    
    print("\n✅ Debug script completed!")
    print("\nNext steps:")
    print("1. If directories were created, restart the app")
    print("2. Check application logs for lead capture attempts")
    print("3. Monitor the logs/leads/ directory for new files")