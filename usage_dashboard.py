#!/usr/bin/env python3
"""
Simple dashboard to check Anthropic API limits and usage
"""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_dashboard():
    """Print a simple usage dashboard"""
    print("\n🌺 Hawaiian Chatbot - API Usage Dashboard")
    print("=" * 60)
    print(f"🕐 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S HST')}")
    print(f"🔑 API Key: {os.getenv('ANTHROPIC_API_KEY', 'Not Set')[:8]}...")
    print()
    
    # Tier Configuration
    tier = os.getenv('ANTHROPIC_TIER', 'build1').lower()
    
    tiers = {
        'free': {
            'name': 'Free Tier',
            'rate_limit': 5,
            'daily_tokens': 300_000,
            'cost': '$0/month'
        },
        'build1': {
            'name': 'Build Tier 1',
            'rate_limit': 50,
            'daily_tokens': 1_000_000,
            'cost': '$5/month'
        },
        'build2': {
            'name': 'Build Tier 2',
            'rate_limit': 1000,
            'daily_tokens': 2_500_000,
            'cost': '$25/month'
        },
        'build3': {
            'name': 'Build Tier 3',
            'rate_limit': 2000,
            'daily_tokens': 5_000_000,
            'cost': '$250/month'
        },
        'build4': {
            'name': 'Build Tier 4',
            'rate_limit': 4000,
            'daily_tokens': 10_000_000,
            'cost': '$1,250/month'
        }
    }
    
    current_tier = tiers.get(tier, tiers['build1'])
    
    print(f"📊 Current Tier: {current_tier['name']} ({current_tier['cost']})")
    print(f"├─ Rate Limit: {current_tier['rate_limit']:,} requests/minute")
    print(f"├─ Daily Tokens: {current_tier['daily_tokens']:,}")
    print("└─ Model: Claude 3 (all models)")
    print()
    
    # Reset Times
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    seconds_to_minute_reset = (next_minute - now).seconds
    
    # Hawaii time for daily reset
    hawaii_hour_offset = -10
    utc_now = datetime.utcnow()
    hawaii_now = utc_now + timedelta(hours=hawaii_hour_offset)
    midnight_hawaii = (hawaii_now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    hours_to_daily_reset = (midnight_hawaii - hawaii_now).total_seconds() / 3600
    
    print("⏱️  Reset Times:")
    print(f"├─ Rate Limit Reset: {seconds_to_minute_reset} seconds ({next_minute.strftime('%H:%M:%S')})")
    print(f"└─ Daily Token Reset: {hours_to_daily_reset:.1f} hours (Midnight HST)")
    print()
    
    # Quick Checks
    print("🔍 Quick Checks:")
    print("├─ Console: https://console.anthropic.com/settings/usage")
    print("├─ Status: https://status.anthropic.com")
    print("└─ Billing: https://console.anthropic.com/settings/plans")
    print()
    
    # If Rate Limited
    print("❓ If You're Rate Limited:")
    print("├─ Wait 60 seconds for rate limit reset")
    print("├─ Upgrade to Build Tier 1 ($5/month) for 10x capacity")
    print("└─ Check if daily token limit (300k) is reached")
    print()
    
    # Usage Tips
    print("💡 Usage Optimization:")
    print("├─ Average conversation: ~400 tokens")
    avg_conversations = current_tier['daily_tokens'] // 400
    hourly_capacity = current_tier['rate_limit'] * 60
    print(f"├─ Daily capacity: ~{avg_conversations:,} conversations")
    print(f"├─ Peak rate: {hourly_capacity:,} conversations/hour")
    print("└─ Use shorter prompts to save tokens")
    print()
    
    # Upgrade Benefits
    print("🚀 Upgrade Benefits (Build Tier 1 - $5/month):")
    print("├─ 50 requests/minute (10x increase)")
    print("├─ 1M tokens/day (3.3x increase)")
    print("├─ ~2,500 daily conversations")
    print("└─ Better for production use")
    print()
    
    print("=" * 60)
    print("✅ For real-time monitoring, run: python monitor_usage.py")
    print("💼 For detailed checks, run: python check_anthropic_limits.py")
    print()


def check_quick_status():
    """Do a quick status check"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ No API key found! Set ANTHROPIC_API_KEY in your .env file")
        return False
    
    print("✅ API key is configured")
    print("🔗 Check your usage at: https://console.anthropic.com/settings/usage")
    return True


if __name__ == "__main__":
    if "--quick" in sys.argv:
        check_quick_status()
    else:
        print_dashboard()
        
    # Show command options
    print("\n📋 Available Commands:")
    print("  python usage_dashboard.py          # Show this dashboard")
    print("  python usage_dashboard.py --quick  # Quick status check")
    print("  python monitor_usage.py            # Live monitoring")
    print("  python check_anthropic_limits.py   # Detailed check")
    print()