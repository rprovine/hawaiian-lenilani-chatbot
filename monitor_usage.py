#!/usr/bin/env python3
"""
Monitor and track Anthropic API usage in real-time
"""
import os
import json
import time
from datetime import datetime, timedelta
from collections import deque
import threading

class UsageMonitor:
    def __init__(self):
        self.requests = deque()  # Track request timestamps
        self.tokens = deque()    # Track token usage
        self.usage_file = "anthropic_usage.json"
        self.load_usage()
        
    def load_usage(self):
        """Load previous usage data"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                    # Convert timestamps back to datetime
                    self.requests = deque([
                        datetime.fromisoformat(ts) for ts in data.get('requests', [])
                    ])
                    self.tokens = deque(data.get('tokens', []))
            except:
                pass
    
    def save_usage(self):
        """Save usage data"""
        data = {
            'requests': [ts.isoformat() for ts in list(self.requests)[-1000:]],  # Keep last 1000
            'tokens': list(self.tokens)[-1000:],
            'last_updated': datetime.now().isoformat()
        }
        with open(self.usage_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def log_request(self, tokens_used=0):
        """Log a new request"""
        now = datetime.now()
        self.requests.append(now)
        if tokens_used > 0:
            self.tokens.append({'timestamp': now.isoformat(), 'tokens': tokens_used})
        self.save_usage()
    
    def get_current_rate(self):
        """Get requests in the last minute"""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        # Clean old requests
        while self.requests and self.requests[0] < one_minute_ago:
            self.requests.popleft()
        
        return len(self.requests)
    
    def get_daily_tokens(self):
        """Get tokens used today"""
        today = datetime.now().date()
        daily_tokens = 0
        
        for token_data in self.tokens:
            ts = datetime.fromisoformat(token_data['timestamp'])
            if ts.date() == today:
                daily_tokens += token_data['tokens']
        
        return daily_tokens
    
    def get_rate_limit_status(self):
        """Get current rate limit status"""
        current_rate = self.get_current_rate()
        daily_tokens = self.get_daily_tokens()
        
        # Free tier limits
        rate_limit = 5
        daily_token_limit = 300000
        
        # Time until rate limit reset
        now = datetime.now()
        next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        seconds_until_reset = (next_minute - now).seconds
        
        # Time until daily reset (midnight HST)
        hawaii_offset = timedelta(hours=-10)
        hawaii_now = now + hawaii_offset
        tomorrow = (hawaii_now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        hours_until_daily_reset = (tomorrow - hawaii_now).total_seconds() / 3600
        
        return {
            'current_requests_per_minute': current_rate,
            'rate_limit': rate_limit,
            'rate_limit_remaining': max(0, rate_limit - current_rate),
            'seconds_until_rate_reset': seconds_until_reset,
            'daily_tokens_used': daily_tokens,
            'daily_token_limit': daily_token_limit,
            'daily_tokens_remaining': max(0, daily_token_limit - daily_tokens),
            'hours_until_daily_reset': round(hours_until_daily_reset, 1),
            'is_rate_limited': current_rate >= rate_limit,
            'is_token_limited': daily_tokens >= daily_token_limit
        }
    
    def display_status(self):
        """Display current status"""
        status = self.get_rate_limit_status()
        
        os.system('clear' if os.name == 'posix' else 'cls')
        print("🌺 Anthropic API Usage Monitor")
        print("=" * 50)
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Rate limit status
        rate_bar = "█" * status['current_requests_per_minute'] + "░" * (status['rate_limit'] - status['current_requests_per_minute'])
        print(f"📊 Rate Limit: [{rate_bar}] {status['current_requests_per_minute']}/{status['rate_limit']} requests/min")
        
        if status['is_rate_limited']:
            print(f"⚠️  RATE LIMITED! Reset in {status['seconds_until_rate_reset']}s")
        else:
            print(f"✅ {status['rate_limit_remaining']} requests available")
        
        print(f"⏱️  Rate reset in: {status['seconds_until_rate_reset']} seconds")
        print()
        
        # Token usage
        token_percent = (status['daily_tokens_used'] / status['daily_token_limit']) * 100
        token_bar_length = 30
        filled = int(token_bar_length * token_percent / 100)
        token_bar = "█" * filled + "░" * (token_bar_length - filled)
        
        print(f"🎯 Daily Tokens: [{token_bar}] {token_percent:.1f}%")
        print(f"   Used: {status['daily_tokens_used']:,} / {status['daily_token_limit']:,}")
        print(f"   Remaining: {status['daily_tokens_remaining']:,}")
        print(f"   Reset in: {status['hours_until_daily_reset']} hours (midnight HST)")
        
        if status['is_token_limited']:
            print("\n⚠️  DAILY TOKEN LIMIT REACHED!")
        
        print("\n💡 Tips:")
        if status['is_rate_limited']:
            print(f"   - Wait {status['seconds_until_rate_reset']}s for rate limit reset")
        if status['is_token_limited']:
            print("   - Wait until midnight HST for token reset")
            print("   - Consider upgrading to a paid tier")
        
        print("\nPress Ctrl+C to exit")


def monitor_live():
    """Run live monitoring"""
    monitor = UsageMonitor()
    
    try:
        while True:
            monitor.display_status()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Aloha! Monitoring stopped.")


def log_usage(tokens=0):
    """Log a request (call this from your app)"""
    monitor = UsageMonitor()
    monitor.log_request(tokens)
    
    status = monitor.get_rate_limit_status()
    if status['is_rate_limited']:
        print(f"⚠️  Rate limited! Wait {status['seconds_until_rate_reset']}s")
        return False
    if status['is_token_limited']:
        print("⚠️  Daily token limit reached!")
        return False
    
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "log":
        # Log a request
        tokens = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        if log_usage(tokens):
            print("✅ Request logged")
        else:
            print("❌ Request blocked by limits")
    else:
        # Run monitoring
        monitor_live()