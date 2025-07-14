#!/usr/bin/env python3
"""
Email Setup Helper for Lead Capture
"""
import os
from dotenv import load_dotenv, set_key

print("🌺 Hawaiian LeniLani Email Setup")
print("=" * 50)
print("\nThis will help you configure email for lead notifications.")
print("\n⚠️  IMPORTANT: For Gmail, you need an App Password, not your regular password!")
print("   1. Go to https://myaccount.google.com/security")
print("   2. Enable 2-factor authentication")
print("   3. Generate an App Password for 'Mail'")
print("   4. Use that password below\n")

# Load current .env
env_file = '.env'
load_dotenv()

# Get current values
current_smtp_user = os.getenv('SMTP_USER', '')
current_lead_email = os.getenv('LEAD_EMAIL', 'reno@lenilani.com')

print("Current configuration:")
print(f"SMTP_USER: {current_smtp_user}")
print(f"LEAD_EMAIL: {current_lead_email}")
print()

# Ask for updates
update = input("Do you want to update the email configuration? (y/n): ").lower().strip()

if update == 'y':
    print("\n📧 Email Provider Setup")
    print("1. Gmail (recommended)")
    print("2. SendGrid")
    print("3. Office 365")
    print("4. Other SMTP")
    
    choice = input("\nSelect your email provider (1-4): ").strip()
    
    if choice == '1':
        # Gmail
        set_key(env_file, 'SMTP_HOST', 'smtp.gmail.com')
        set_key(env_file, 'SMTP_PORT', '587')
        
        email = input("Enter your Gmail address: ").strip()
        set_key(env_file, 'SMTP_USER', email)
        
        app_password = input("Enter your Gmail App Password (NOT regular password): ").strip()
        set_key(env_file, 'SMTP_PASSWORD', app_password)
        
    elif choice == '2':
        # SendGrid
        set_key(env_file, 'SMTP_HOST', 'smtp.sendgrid.net')
        set_key(env_file, 'SMTP_PORT', '587')
        set_key(env_file, 'SMTP_USER', 'apikey')
        
        api_key = input("Enter your SendGrid API key: ").strip()
        set_key(env_file, 'SMTP_PASSWORD', api_key)
        
    elif choice == '3':
        # Office 365
        set_key(env_file, 'SMTP_HOST', 'smtp.office365.com')
        set_key(env_file, 'SMTP_PORT', '587')
        
        email = input("Enter your Office 365 email: ").strip()
        set_key(env_file, 'SMTP_USER', email)
        
        password = input("Enter your Office 365 password: ").strip()
        set_key(env_file, 'SMTP_PASSWORD', password)
        
    else:
        # Custom SMTP
        host = input("Enter SMTP host: ").strip()
        set_key(env_file, 'SMTP_HOST', host)
        
        port = input("Enter SMTP port (usually 587 or 465): ").strip()
        set_key(env_file, 'SMTP_PORT', port)
        
        user = input("Enter SMTP username/email: ").strip()
        set_key(env_file, 'SMTP_USER', user)
        
        password = input("Enter SMTP password: ").strip()
        set_key(env_file, 'SMTP_PASSWORD', password)
    
    # Lead email
    lead_email = input(f"\nWhere should leads be sent? [{current_lead_email}]: ").strip()
    if not lead_email:
        lead_email = current_lead_email
    set_key(env_file, 'LEAD_EMAIL', lead_email)
    
    print("\n✅ Email configuration updated!")
    print("\n⚠️  IMPORTANT: Restart the backend for changes to take effect:")
    print("   ./start_backend.sh")
    
else:
    print("\n❌ Email configuration not updated.")
    print("\nTo receive lead notifications, you need to:")
    print("1. Set SMTP_USER to your actual email")
    print("2. Set SMTP_PASSWORD to your app password")
    print("3. Add LEAD_EMAIL=reno@lenilani.com to your .env file")

print("\n🧪 To test email after configuration:")
print("   python test_lead_capture.py")