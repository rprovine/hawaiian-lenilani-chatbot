"""
Enhanced rate limit handling for Claude API
"""
import time
import logging
from typing import Optional, Dict, Any
from functools import wraps
import random

logger = logging.getLogger(__name__)


class RateLimitHandler:
    """Handles rate limiting and backoff strategies"""
    
    def __init__(self):
        self.last_request_time = 0
        self.consecutive_errors = 0
        self.min_request_interval = 1.5  # Minimum seconds between requests
        
    def wait_if_needed(self):
        """Enforce minimum time between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            wait_time = self.min_request_interval - elapsed
            logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
            time.sleep(wait_time)
        self.last_request_time = time.time()
    
    def handle_error(self, error: Exception) -> Optional[float]:
        """
        Handle API errors and return wait time if retry is appropriate
        Returns None if error is not retryable
        """
        error_str = str(error)
        
        if "529" in error_str or "overloaded" in error_str.lower():
            self.consecutive_errors += 1
            # Exponential backoff with jitter
            base_wait = min(30, 2 ** self.consecutive_errors)
            jitter = random.uniform(0, base_wait * 0.1)
            wait_time = base_wait + jitter
            
            logger.warning(f"API overloaded (attempt {self.consecutive_errors}), waiting {wait_time:.1f}s")
            return wait_time
        
        elif "429" in error_str:  # Rate limit
            self.consecutive_errors += 1
            wait_time = 60  # Wait a full minute for rate limits
            logger.warning(f"Rate limit hit, waiting {wait_time}s")
            return wait_time
        
        else:
            # Non-retryable error
            logger.error(f"Non-retryable error: {error}")
            return None
    
    def reset_errors(self):
        """Reset error counter on successful request"""
        self.consecutive_errors = 0
    
    def get_backoff_multiplier(self) -> float:
        """Get current backoff multiplier based on error count"""
        return min(5.0, 1.0 + (self.consecutive_errors * 0.5))


def with_rate_limit(handler: RateLimitHandler):
    """Decorator to add rate limiting to API calls"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    # Wait if needed before making request
                    handler.wait_if_needed()
                    
                    # Make the API call
                    result = await func(*args, **kwargs)
                    
                    # Success - reset error counter
                    handler.reset_errors()
                    return result
                    
                except Exception as e:
                    wait_time = handler.handle_error(e)
                    
                    if wait_time is None or attempt == max_retries - 1:
                        # Non-retryable error or last attempt
                        raise
                    
                    # Wait and retry
                    time.sleep(wait_time)
            
            # Should not reach here
            raise Exception("Max retries exceeded")
        
        return wrapper
    return decorator


# Singleton instance
rate_limiter = RateLimitHandler()