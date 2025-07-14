#!/usr/bin/env python3
"""
Check Anthropic API rate limits and usage
"""
import os
import sys
import json
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from anthropic import Anthropic
import requests

# Load environment variables
load_dotenv()

class AnthropicUsageChecker:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            print("❌ Error: ANTHROPIC_API_KEY not found in environment variables")
            sys.exit(1)
        
        self.client = Anthropic(api_key=self.api_key)
        
    def check_rate_limits(self):
        """Check current rate limits by making a small test request"""
        print("🔍 Checking Anthropic API Rate Limits...")
        print("=" * 50)
        
        try:
            # Make a minimal request to check headers
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Use cheapest model
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            
            print("✅ API is accessible")
            print(f"📝 Response: {response.content[0].text}")
            
            # Note: Anthropic API doesn't return rate limit headers in responses
            # We need to track usage through their console or implement our own tracking
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error: {error_msg}")
            
            # Parse rate limit errors
            if "rate_limit_error" in error_msg or "429" in error_msg:
                print("\n⚠️  Rate Limit Hit!")
                self._parse_rate_limit_error(error_msg)
            elif "529" in error_msg:
                print("\n⚠️  API Overloaded - Please try again later")
            else:
                print(f"\n❌ Unexpected error: {error_msg}")
    
    def _parse_rate_limit_error(self, error_msg):
        """Parse rate limit error message for details"""
        # Anthropic typically includes retry-after in errors
        if "retry" in error_msg.lower():
            print("💡 Check the error message for retry-after time")
        
        # Calculate reset time (rate limits reset every minute)
        now = datetime.now()
        next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        seconds_until_reset = (next_minute - now).seconds
        
        print(f"⏱️  Rate limit likely resets in: {seconds_until_reset} seconds")
        print(f"🕐 Reset time: {next_minute.strftime('%H:%M:%S')}")
    
    def estimate_usage(self):
        """Estimate usage based on common patterns"""
        print("\n📊 Usage Estimation Guide")
        print("=" * 50)
        
        # Free tier limits
        print("🆓 Free Tier Limits:")
        print("  - 5 requests per minute")
        print("  - 300,000 tokens per day")
        print("  - ~1,000 average conversations per day")
        
        # Token estimation
        print("\n📏 Token Usage Estimation:")
        print("  - Average greeting: ~100-200 tokens")
        print("  - Average conversation: ~300-500 tokens")
        print("  - Long conversation: ~1,000-2,000 tokens")
        
        # Calculate daily capacity
        print("\n📈 Daily Capacity (Free Tier):")
        avg_tokens_per_conversation = 400
        daily_conversations = 300000 / avg_tokens_per_conversation
        print(f"  - Estimated conversations: ~{int(daily_conversations)}")
        print(f"  - With rate limit: max 5 conversations/minute")
        print(f"  - Effective hourly limit: ~300 conversations")
    
    def check_api_status(self):
        """Check Anthropic API status"""
        print("\n🌐 Checking Anthropic API Status...")
        print("=" * 50)
        
        try:
            # Check if we can reach Anthropic
            response = requests.get("https://api.anthropic.com", timeout=5)
            if response.status_code == 403:  # Expected for root endpoint
                print("✅ Anthropic API is reachable")
            else:
                print(f"⚠️  Unexpected status code: {response.status_code}")
        except Exception as e:
            print(f"❌ Cannot reach Anthropic API: {e}")
        
        print("\n💡 For real-time status, visit: https://status.anthropic.com")
    
    def show_recommendations(self):
        """Show recommendations based on usage"""
        print("\n💡 Recommendations")
        print("=" * 50)
        
        print("1. 🔍 Monitor Usage:")
        print("   - Visit: https://console.anthropic.com/settings/usage")
        print("   - Check your daily token usage")
        print("   - Review request patterns")
        
        print("\n2. 🚀 If Hitting Limits:")
        print("   - Wait 60 seconds (rate limit reset)")
        print("   - Upgrade to Build Tier 1 ($5/month)")
        print("   - Implement request queueing")
        
        print("\n3. 💰 Tier Comparison:")
        print("   - Free: 5 req/min, 300k tokens/day")
        print("   - Tier 1 ($5): 50 req/min, 1M tokens/day")
        print("   - Tier 2 ($25): 1,000 req/min, 2.5M tokens/day")
    
    def run_full_check(self):
        """Run all checks"""
        print("🌺 Hawaiian Chatbot - Anthropic API Usage Checker")
        print("=" * 50)
        print(f"🕐 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔑 API Key: {self.api_key[:8]}...{self.api_key[-4:]}")
        print()
        
        # Run all checks
        self.check_api_status()
        self.check_rate_limits()
        self.estimate_usage()
        self.show_recommendations()
        
        print("\n✅ Check complete!")
        print("\n🌺 Aloha! Remember to check the Anthropic Console for accurate usage data.")


def main():
    """Main function"""
    checker = AnthropicUsageChecker()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "quick":
            checker.check_rate_limits()
        elif command == "status":
            checker.check_api_status()
        elif command == "usage":
            checker.estimate_usage()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python check_anthropic_limits.py [quick|status|usage]")
    else:
        checker.run_full_check()


if __name__ == "__main__":
    main()